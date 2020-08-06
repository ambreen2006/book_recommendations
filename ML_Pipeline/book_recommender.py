import numpy as np

from random import choice
from collections import OrderedDict
from collections import defaultdict

import heapq

import os
import sys

if (current_path := os.getcwd()) not in sys.path:
    sys.path.append(str(current_path))
    print('Appending path of the parent directory for module imports: ',
          current_path)

from ML_Pipeline.data_loader import BooksDataLoader


def leave_one_out(x):
    """Takes one element out of the given set randomly.

    :param x: The set from which an element is to be removed
    :return:
    x - modified set
    left_out - the element that was removed
    """

    left_out = choice(list(x))
    x.remove(left_out)
    return x, left_out


def partition(X):
    """Partition each set in the list such that the modified set has one item less.
    :param X: The list of set to be modified.
    :return:
    new_list: Modified list of sets
    left_out_list: The list of items that was removed from the original list of sets.
    """

    new_list = []
    left_out_list = []

    for x in X:
        new_x, left_out = leave_one_out(x)
        new_list.append(new_x)
        left_out_list.append(left_out)

    return new_list, left_out_list


def hit_rate(predicted_list, left_out_list):
    """Calculate hit rate by counting how many times the left_out item was predicted in
    recommendation"""

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
    """Book Recommender Class"""

    def __init__(self, base_dir=''):

        data_loader = BooksDataLoader(base_dir)
        self.genre_similarity = data_loader.get_genre_similarity_matrix()
        self.genre_similarity.columns = self.genre_similarity.columns.astype(int)

        self.available_books = set(self.genre_similarity.columns.values)
        self.books_data = data_loader.get_books_data()
        self.books_genre = data_loader.get_books_genre().set_index('book_id')

    def get_book_rating(self, book):
        """Get the average book rating of the book specified by book_id"""

        avg_rating = self.books_data.loc[self.books_data.book_id == book,
                                         'average_rating'].values[0]
        return avg_rating

    def get_books_similarity(self, book_id_1, book_id_2):
        """Get cosine similarity score between two books"""

        return self.genre_similarity.loc[self.genre_similarity.index == book_id_1,
                                         book_id_2].values[0]

    def get_books_available(self):
        """List of available book id's"""

        return self.available_books

    def get_genres_cardinality(self, book_list):

        return self.books_genre[self.books_genre.index.isin(book_list)] \
            .sum().to_dict()

    def get_top_recommendations(self, book_recommendations, k=10):
        """Get Top-K recommendations by discouraging already recommended authors
        :param book_recommendations: The original book_recommendations with scores
        :param k: The number of recommendations requested
        :returns the ordered book list without the score information
        """

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
        """Make book recommendations
        :param user_list: list of user id's
        :param reviewed_books_list: set of books reviewed by the user
        :param user_reviewed_books_rating: user rating of each book reviewed
        :param threshold: similarity threshold for filtering
        :param rating_threshold: rating threshold for filtering"""

        def get_author_for_book(book):
            """Get the author name of the given book by book_id"""

            return self.books_data[self.books_data.book_id == book].authors.values[0]

        def get_authors(book_list):
            """Get the authors for the books in the book list"""

            authors = set(self.books_data[self.books_data.book_id.isin(book_list)].authors.values)
            return authors

        def get_author_weight(book, authors):
            """Get the weight based on authors of the book for user personalization"""

            book_author = get_author_for_book(book)
            if book_author in authors:
                return 3
            else:
                return 1

        def get_ratings_weight(book):
            """Get smoothed rating weight of the book"""

            rating = self.get_book_rating(book)
            if rating < 3:
                return 1
            elif rating > 4:
                return 3
            else:
                return 2

        def get_user_book_weight(book, user_rating, max_similar_book):
            """Get weight based on the most similar user reviewed book"""

            similar_book = max_similar_book[book]
            weight = user_rating[similar_book]
            return weight

        def get_max_similarity(book, comparing_book_list):
            """Get the maximum similarity score to the user's book"""

            max_sim = self.genre_similarity.loc[self.genre_similarity.index == book,
                                                comparing_book_list].max(axis=1).values[0]
            index = self.genre_similarity.loc[self.genre_similarity.index == book,
                                              comparing_book_list].idxmax(axis=1).values[0]
            return max_sim, index

        train_size = len(user_list)

        recommended_books = []
        # Starting with user
        for i in range(0, train_size):

            reviewed_books = set(reviewed_books_list[i])
            user_rating = user_reviewed_books_rating[i]
            available_books_unreviewed = self.available_books - reviewed_books

            book_similarity = defaultdict(int)
            max_similar_book = dict()

            read_authors = get_authors(reviewed_books)

            score = dict()

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

            recommended_books.append(OrderedDict(sorted(score.items(),
                                                        key=lambda v: v[1], reverse=True)))

        return recommended_books
