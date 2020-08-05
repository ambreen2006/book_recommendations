import pandas as pd
import sqlalchemy as db


class BooksDataLoader(object):

    def __init__(self,
                 base_dir='',
                 readers_path='Data/goodbooks-10k/ratings.csv',
                 genre_similarity_matrix_path='Data/genre_similarity_matrix_df.csv',
                 books_meta_data_path='Data/books.db',
                 books_genre_data_path='Data/books_genre_df.csv',
                 books_path='Data/goodbooks-10k/books.csv'):

        self.connection = None
        self.books_data = None
        self.books_genre = None
        self.readers_data = None
        self.books_meta_data = None
        self.genre_similarity_matrix = None

        self.books_path = base_dir + books_path
        self.readers_path = base_dir + readers_path
        self.books_genre_path = base_dir + books_genre_data_path
        self.books_meta_data_path = base_dir + books_meta_data_path
        self.genre_similarity_matrix_path = base_dir + genre_similarity_matrix_path

    def load_genre_similarity_matrix(self):

        assert self.genre_similarity_matrix_path, "Path to the data file needs to be provided"
        self.genre_similarity_matrix = pd.read_csv(self.genre_similarity_matrix_path)
        self.genre_similarity_matrix.set_index('book_id', inplace=True)

    def load_books_genre(self):

        assert self.books_genre_path, "Path to the data file needs to be provided"
        self.books_genre = pd.read_csv(self.books_genre_path)

    def load_readers_data(self):

        assert self.readers_path, "Path to the data file needs to be provided"
        self.readers_data = pd.read_csv(self.readers_path)

    def load_books_data(self):

        assert self.readers_path, "Path to the data file needs to be provided"
        self.books_data = pd.read_csv(self.books_path)

    def load_books_meta_data(self):

        assert self.books_meta_data_path, "Path to the data file needs to be provided"

        db_path = 'sqlite:///' + self.books_meta_data_path
        db_engine = db.create_engine(db_path)
        self.connection = db_engine.connect()
        self.books_meta_data = pd.read_sql_table('books_meta_data', self.connection)

    def get_readers_data(self):

        if self.readers_data is None:
            self.load_readers_data()

        return self.readers_data

    def get_genre_similarity_matrix(self):

        if self.genre_similarity_matrix is None:
            self.load_genre_similarity_matrix()

        return self.genre_similarity_matrix

    def get_books_genre(self):

        if self.books_genre is None:
            self.load_books_genre()

        return self.books_genre

    def get_books_data(self):

        if self.books_data is None:
            self.load_books_data()

        return self.books_data

    def get_books_meta_data(self):

        if self.books_meta_data is None:
            self.load_books_meta_data()

        return self.books_meta_data

    def get_book_details_by_id(self, book_id_list):

        books = self.get_books_data()
        return books[books.book_id.isin(book_id_list)]
