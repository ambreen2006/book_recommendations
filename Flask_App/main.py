import sys
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = '<replace>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b"<replace>"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facebook_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    def __init__(self, facebook_id, facebook_name):
        self.facebook_id = facebook_id
        self.name = facebook_name


class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    rating = db.Column(db.Float)
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id'),)

    def __init__(self, user_id, book_id, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating


db.create_all()
db.session.commit()

parent_path = Path(__file__).resolve().parent.parent
print('Appending path of the parent directory for module imports: ',
      parent_path)

sys.path.append(str(parent_path))

from ML_Pipeline.data_loader import BooksDataLoader
from ML_Pipeline.book_recommender import BookRecommender

books_data_loader = BooksDataLoader()

recommender = BookRecommender()
available_books_ids = list(map(int, recommender.get_books_available()))
available_books = books_data_loader.get_book_details_by_id(available_books_ids)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    print("Method = ", request.method)
    if request.method == 'POST':
        print('getting data')
        data = request.get_json()
        print('json data: ', data)

        fb_id = data['id']
        fb_name = data['name']

        if fb_id == '':
            return render_template('index.html')

        if db.session.query(User).filter(User.facebook_id == fb_id).count() == 0:
            new_user = User(fb_id, fb_name)
            db.session.add(new_user)
            db.session.commit()

        current_user = db.session.query(User).filter_by(facebook_id=fb_id).first()
        session['user_id'] = current_user.id
        session['user_name'] = current_user.name

        return {'success': True}

    return render_template('index.html')


@app.route('/home', methods=['GET'])
def home_page():

    if 'user_id' not in session:
        return render_template('index.html')

    if 'user_name' in session:
        user_name = session['user_name']

    if 'user_id' in session:
        user_id = session['user_id']
        print('Found user', user_id)

    books_rating = db.session.query(Rating).filter_by(user_id=user_id).all()
    books_rating_dict = {r.book_id: r.rating for r in books_rating}

    books = available_books.loc[available_books.book_id.isin(books_rating_dict.keys()),
                                ['title', 'authors', 'book_id']]

    return render_template('home.html',
                           book_list=books.to_dict(orient='records'),
                           user_name=user_name,
                           books_rating_dict=books_rating_dict)


@app.route('/search', methods=['POST', 'GET'])
def search():

    if 'user_id' not in session:
        return render_template('index.html')

    if 'user_name' in session:
        user_name = session['user_name']

    user_id = session['user_id']

    if request.method == 'POST':
        search_term = request.form['search'].lower()
        print('Searching for: ', search_term)
        print(available_books.head())

        # find books that matches the Search
        found_books = available_books.loc[(available_books.title.str.contains(search_term, case=False)) | \
                                          (available_books.authors.str.contains(search_term, case=False)),
                                          ['title', 'authors', 'book_id', 'image_url', 'average_rating']]

        # search book ratings of the user
        books_rating = db.session.query(Rating).filter_by(user_id=user_id).all()
        books_rating_dict = {r.book_id: r.rating for r in books_rating}

        return render_template('search.html',
                               book_list=found_books.to_dict(orient='records'),
                               user_name=user_name,
                               books_rating_dict=books_rating_dict)
    else:
        return render_template('search.html',
                               user_name=user_name)


@app.route('/rating', methods=['POST', 'PUT', 'DELETE'])
def store_user_preference():
    print('Creating ratings')

    if 'user_id' not in session:
        return render_template('index.html')

    user_id = session['user_id']

    data = request.get_json()
    selected_book = data['book_id']
    user_rating = data['rating']

    if request.method == 'POST':
        print('Creating new rating for book')
        # Creating Rating object
        rating = Rating(user_id, selected_book, user_rating)
        db.session.add(rating)
        db.session.commit()
        return make_response('Success', 201)

    elif request.method == 'PUT':
        print('Modifying existing rating for book')
        existing_rating = db.session.query(Rating).filter_by(user_id=user_id,
                                                             book_id=selected_book).first()
        existing_rating.rating = user_rating
        db.session.commit()
        return make_response('Success', 200)

    elif request.method == 'DELETE':
        print('Deleting existing rating for book')
        existing_rating = db.session.query(Rating).filter_by(user_id=user_id,
                                                             book_id=selected_book).first()
        db.session.delete(existing_rating)
        db.session.commit()
        return make_response('Success', 200)

@app.route('/recommend', methods=['GET'])
def make_recommendations():

    print('/recommend')
    if 'user_id' not in session:
        return render_template('index.html')

    if 'user_name' in session:
        user_name = session['user_name']

    user_id = session['user_id']

    print('user_id', user_id)

    rating_list = db.session.query(Rating).filter_by(user_id=user_id).all()
    if (len(rating_list) == 0):
        return render_template('no_personal_selection.html')

    selected_books = [rating.book_id for rating in rating_list if rating.rating >= 3]
    user_ratings = {rating.book_id: rating.rating for rating in rating_list}

    print('User rating', user_ratings)
    recommended_books = recommender.recommend([user_id],
                                              [selected_books],
                                              [user_ratings])[0]

    recommended_books = recommender.get_top_recommendations(recommended_books, k=50)
    print(recommended_books)

    top_md = pd.DataFrame(columns=['book_id', 'title', 'authors', 'average_rating'])

    for book in recommended_books:
        top_md = top_md.append(
            available_books.loc[available_books.book_id == book,
                                ['book_id', 'title', 'authors', 'average_rating']])

    return render_template('recommendations.html',
                           book_list=top_md.to_dict(orient='records'),
                           user_name=user_name)


if __name__ == '__main__':
    print('Starting recommender app')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgpass@localhost/written_words'
    app.debug = True
    app.run()