from collections import defaultdict
from functools import partial
from random import choice

from data_loader import BooksDataLoader


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

        if str(left_out) in predicted:
            hit_count += 1

    rate = hit_count / total
    return rate


class BookRecommender(object):

    def __init__(self):

        self.genre_similarity = BooksDataLoader().get_genre_similarity_matrix()

    def recommend(self, user_list, reviewed_books_list):

        def filter_book(b, col):

            val = self.genre_similarity.loc[self.genre_similarity.index == b, col].values[0]
            if val >= 0.4:
                return True
            else:
                return False

        train_size = len(user_list)
        available_books = self.genre_similarity.columns.values

        recommended_books = []
        for i in range(0, train_size):

            user = user_list[i]
            reviewed_books = reviewed_books_list[i]

            recommend_to_user = set()
            for book in reviewed_books:
                similar_books = set(filter(partial(filter_book, int(book)), available_books))
                recommend_to_user.update(similar_books)

            recommend_to_user = recommend_to_user - set(reviewed_books)
            recommended_books.append(recommend_to_user)

        return recommended_books
