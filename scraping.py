import requests
from bs4 import BeautifulSoup

SITE_LIST = {
    'Nature': 'https://www.nature.com/news',
    'Science': 'https://www.science.org/news'
}

nature_response = requests.get(SITE_LIST['Nature'])
science_response = requests.get(SITE_LIST['Science'])

nature_soup = BeautifulSoup(nature_response.text, 'html.parser')
science_soup = BeautifulSoup(science_response.text, 'html.parser')


all_links = [
    str(link.get('href')) for link in nature_soup.find_all('a')
    if str(link.get('href')).startswith('https')
]
article_links = [link for link in all_links if 'articles' in link]
print(article_links)
