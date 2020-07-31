import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#ENV = 'DEVELOPMENT'
ENV = 'RELEASE'

if ENV == 'DEVELOPMENT':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:whateverpass2020@localhost/written_words'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hcjptrgngifrjk:4621bd3221e1e60d55be828015368cdc4e09f52e5fe6c5274bcae7d6d68c58c4@ec2-107-20-104-234.compute-1.amazonaws.com:5432/de7f4pcsnnpa37'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b"\xef\xf2\x8aj\x04q\xa0Y\x90'\xbf\n8\x8aa\n"

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facebook_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    def __init__(self, facebook_id, facebook_name):
        self.facebook_id = facebook_id
        self.name = facebook_name

parent_path = Path(__file__).resolve().parent.parent
print('Appending path of the parent directory for module imports: ',
       parent_path)

sys.path.append(str(parent_path))

from ML_Pipeline.data_loader import BooksDataLoader
from ML_Pipeline.book_recommender import BookRecommender

books_data_loader = BooksDataLoader()
recommender = BookRecommender()
available_books_ids = list(map(int, recommender.books_available()))
print(available_books_ids)
available_books = books_data_loader.get_book_details_by_id(available_books_ids)
print(available_books.columns.values)
print(available_books.head().title)

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

@app.route('/home', methods=['POST', 'GET'])
def home_page():

    #TODO If not authorized, redirect to index

    user_name = session['user_name']

    if request.method == 'POST':
        search_term =  request.form['search'].lower()
        print('Searching for: ', search_term)
        print(available_books.head())
        found_books = available_books.loc[available_books.title.str.contains(search_term, case=False),
        ['title']]
        return render_template('home.html',
                                book_list=found_books[:10].title,
                                user_name=user_name)

    return render_template('home.html', user_name=user_name)


if __name__ == '__main__':

    app.run(debug=True)
