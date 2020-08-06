import json
import urllib.request
from Python_SQLite_Helper.SQLiteHelper import SQLiteHelper

from bs4 import BeautifulSoup


class DataExtractor:
    '''DataExtractor parses the web page and insert the relevent content into the database'''

    def __init__(self):

        self.db_helper = SQLiteHelper('../Data/books.db')
        fields_info = {
            'book_id': 'INTEGER',
            'genre': 'TEXT',
            'description': 'TEXT'
        }

        result, _ = self.db_helper.create('books_meta_data', fields_info)
        if result:
            print("Table books_meta_data Exist or Created")

    def extract_using_api(self, author=None, book_id_with_title=None):
        '''Extract information using the Google Books API'''

        assert author, "Author must be provided"
        assert book_id_with_title, "book_id_with_title must be provided"

        base_url = "https://www.googleapis.com/books/v1/volumes?"

        for i in range(0, len(book_id_with_title)):
            book_id = book_id_with_title[i][0]
            title = book_id_with_title[i][1]
            url = base_url + 'q=intitle:"' + title.replace(' ', '+') + '"+inauthor:"' + author.replace(' ', '+') + '"'

            with urllib.request.urlopen(url) as response:
                source = response.read()
                data = json.loads(source)
                print(data)
                if "items" not in data:
                    print("Failed in finding: " + title)
                    continue

                for book in data['items']:
                    volumeInfo = book['volumeInfo']
                    if volumeInfo['title'] == title and author in volumeInfo['authors']:
                        print("Found: " + title)
                        description = ""
                        if "description" in volumeInfo:
                            description = volumeInfo['description']
                        categories = ""
                        if 'categories' in volumeInfo:
                            categories = (' / '.join(volumeInfo['categories'])).title()
                        self.db_helper.insert('books_meta_data', {'book_id': book_id,
                                                                  'genre': categories,
                                                                  'description': description})

    def extract_from_url(self, id_to_page=None):
        '''Extract information by scraping the web page'''

        assert id_to_page, "id_to_page should be a valid mapping"

        for i in range(0, len(id_to_page)):
            url = id_to_page[i][1]
            print("Extracting: " + str(id_to_page[i][0]))
            with urllib.request.urlopen(url) as response:
                book_html = response.read()
                soup = BeautifulSoup(book_html, "html.parser")
                book_genre = ''
                book_description = ''
                for element in soup.find_all(attrs={'class': 'hAyfc'}):
                    enclosing_text = element.div.get_text()
                    if enclosing_text == 'Genres':
                        for genre_element in element.find_all(attrs={'class': 'htlgb'}):
                            book_genre += genre_element.get_text() + ' '
                for element in soup.find_all(attrs={'class': 'W4P4ne'}):
                    meta_description = element.find('meta')
                    if meta_description:
                        book_description = meta_description['content']

            self.db_helper.insert('books_meta_data', {'book_id': id_to_page[i][0],
                                                      'genre': book_genre,
                                                      'description': book_description})
