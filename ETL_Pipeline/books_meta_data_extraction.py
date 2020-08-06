import sys
import pandas as pd

sys.path.append(".")

from data_extractor import DataExtractor

sub_books = pd.read_csv('../Data/sub_authors_us_100_200.csv')
sub_books = sub_books.drop(columns=['authors', 'original_title'])
id_to_urls = sub_books.values.tolist()
de = DataExtractor()
de.extract_from_url(id_to_urls)