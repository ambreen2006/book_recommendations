import numpy as np

from random import choice
from collections import OrderedDict
from collections import defaultdict

import heapq

import os
import sys

# print('Current Path', os.getcwd())
# print('syspath', sys.path)

if (current_path := os.getcwd()) not in sys.path:
    sys.path.append(str(current_path))
    print('Appending path of the parent directory for module imports: ',
          current_path)

from ML_Pipeline.data_loader import BooksDataLoader


def leave_one_out(x):
    left_out = choice(list(x))
    x.remove(left_out)
    return x, left_out


def partition(X):
    new_list = []
    left_out_list = []

    for x in X:
        new_x, left_out = leave_one_out(x)
        new_list.append(new_x)
        left_out_list.append(left_out)

    return new_list, left_out_list


def hit_rate(predicted_list, left_out_list):
    total = len(predicted_list)
    hit_count = 0

    for i in range(0, total):
        predicted = predicted_list[i]
        left_out = left_out_list[i]

        if left_out in predicted:
            hit_count += 1

    rate = hit_count / total
    return rate


class BookRecommender(object):

    def __init__(self, base_dir=''):

        data_loader = BooksDataLoader(base_dir)
        self.genre_similarity = data_loader.get_genre_similarity_matrix()
        self.genre_similarity.columns = self.genre_similarity.columns.astype(int)

        self.available_books = set(self.genre_similarity.columns.values)
        self.books_data = data_loader.get_books_data()
        self.books_genre = data_loader.get_books_genre().set_index('book_id')

    def get_book_rating(self, book):

        avg_rating = self.books_data.loc[self.books_data.book_id == book,
                                         'average_rating'].values[0]
        return avg_rating

    def get_books_similarity(self, book_id_1, book_id_2):

        return self.genre_similarity.loc[self.genre_similarity.index == book_id_1,
                                         book_id_2].values[0]

    def get_books_available(self):

        return self.available_books

    def get_genres_cardinality(self, book_list):

        return self.books_genre[self.books_genre.index.isin(book_list)] \
            .sum().to_dict()

    def get_top_recommendations(self, book_recommendations, k=10):

        top_k = []
        authors_cardinality = defaultdict(lambda: 1)

        for book in book_recommendations:
            authors = self.books_data.loc[self.books_data.book_id == book, 'authors'].values[0]
            authors_cardinality[authors] += 1
            priority = -1 * book_recommendations[book] * (1 / authors_cardinality[authors])
            heapq.heappush(top_k, (priority, book))
            if len(top_k) >= k:
                break

        return [book_tuple[1] for book_tuple in top_k]

    def recommend(self,
                  user_list,
                  reviewed_books_list,
                  user_reviewed_books_rating,
                  threshold=0.1,
                  rating_threshold=3):

        def get_genres_for_book(book):

            def condition(x):
                if self.books_genre.loc[self.books_genre.index == book, x].values[0] == 1:
                    return True
                else:
                    return False

            condition_list = list(map(condition, self.books_genre.columns.values))
            loc = np.where(self.books_genre.index == book)[0][0]
            return self.books_genre.iloc[loc, condition_list].index.values

        def get_author_for_book(book):

            return self.books_data[self.books_data.book_id == book].authors.values[0]

        def get_authors(book_list):

            # print('book_list', book_list)
            authors = set(self.books_data[self.books_data.book_id.isin(book_list)].authors.values)
            # print('authors', authors)
            return authors

        def get_author_weight(book, authors):

            book_author = get_author_for_book(book)
            if book_author in authors:
                # print('Found book author', book_author)
                return 3
            else:
                return 1

        def get_ratings_weight(book):

            rating = self.get_book_rating(book)
            if rating < 3:
                return 1
            elif rating > 4:
                return 3
            else:
                return 2

        def get_genre_weights(user_genres, book):

            book_genre = get_genres_for_book(book)
            weight = 1  # so in case of no match default genre weight is 1
            for genre in book_genre:
                if user_genres[genre] > 0:
                    weight += 1

            return weight

        def get_user_book_weight(book, user_rating, max_similar_book):

            similar_book = max_similar_book[book]
            weight = user_rating[similar_book]
            # print('Max Similar Book', similar_book, 'sim', 'rating', weight)
            return weight

        def get_max_similarity(book, comparing_book_list):

            max_sim = self.genre_similarity.loc[self.genre_similarity.index == book,
                                                comparing_book_list].max(axis=1).values[0]
            index = self.genre_similarity.loc[self.genre_similarity.index == book,
                                              comparing_book_list].idxmax(axis=1).values[0]
            # print('max_sim', max_sim)
            # print('max_sim index', index.values[0])
            # print('max_sim val', max_sim.values[0])
            # print('max_sim', max_sim)
            return max_sim, index

        train_size = len(user_list)

        recommended_books = []
        # Starting with user
        for i in range(0, train_size):

            user = user_list[i]
            reviewed_books = set(reviewed_books_list[i])
            user_rating = user_reviewed_books_rating[i]
            available_books_unreviewed = self.available_books - reviewed_books

            book_similarity = defaultdict(int)
            max_similar_book = dict()

            books_genre = self.get_genres_cardinality(reviewed_books)
            read_authors = get_authors(reviewed_books)

            # print('UserID', user)
            # print('user_rating', user_rating)
            score = dict()
            # recommend_to_user = set()

            for col in available_books_unreviewed:
                if self.get_book_rating(col) >= rating_threshold:
                    similarity, similar_book = get_max_similarity(col, list(reviewed_books))
                    book_similarity[col] = similarity
                    max_similar_book[col] = similar_book

            # filter out books with low similarity values
            book_similarity = {k: v for k, v in book_similarity.items() if v >= threshold}

            for book in book_similarity:
                score[book] = book_similarity[book] \
                              * get_author_weight(book, read_authors) \
                              * get_ratings_weight(book) \
                              * get_user_book_weight(book, user_rating, max_similar_book)

                """
                score[book] = book_similarity[book] * \
                                   self.get_book_rating(book) * \
                                   get_genre_weights(books_genre, book)
                """

            recommended_books.append(OrderedDict(sorted(score.items(),
                                                        key=lambda v: v[1], reverse=True)))

        return recommended_books


'''
class BookRecommender_old(object):

    def __init__(self):

        data_loader = BooksDataLoader()
        self.genre_similarity = data_loader.get_genre_similarity_matrix()
        self.books_data = data_loader.get_books_data()

    def books_available(self):

        return self.genre_similarity.columns.values

    def recommend(self, user_list, reviewed_books_list, threshold = 0.4):

        def filter_book(b, col):

            book_rating = self.books_data.loc[self.books_data.book_id == int(col), 'average_rating'].values[0]
            if book_rating < 3:
                print('book discarding', 'book_id', col, 'rating', book_rating)
                return False

            val = self.genre_similarity.loc[self.genre_similarity.index == b, col].values[0]
            if val >= threshold:
                return True
            else:
                return False

        train_size = len(user_list)
        available_books = list(self.books_available())

        recommended_books = []
        for i in range(0, train_size):

            user = user_list[i]
            reviewed_books = reviewed_books_list[i]

            recommend_to_user = set()
            for book in reviewed_books:
                filtered_books = set(col for col in available_books if filter_book(book, col))
                recommend_to_user.update(filtered_books)

            recommend_to_user = set(map(int, recommend_to_user))
            recommend_to_user = recommend_to_user - set(reviewed_books)
            recommended_books.append(recommend_to_user)

        return recommended_books
'''
