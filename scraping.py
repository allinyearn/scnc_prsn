from bs4 import BeautifulSoup
from test_data import html_doc

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
