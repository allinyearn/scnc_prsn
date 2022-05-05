def get_data():
    req = requests.get('http://feeds.nature.com/nature/rss/current')
    soup = BeautifulSoup(req.text, 'xml')
    useless_subs = ['<dc:', 'nature.com', '>Nature<']
    titles = [str(title) for title in soup.find_all('title')]
    processed_titles = []
    links = [
        str(link)[6:-7] for link in soup.find_all('link')
        if '//feeds' not in str(link) and
        'atom' not in str(link)
    ]
    for title in titles:
        flag = False
        for substring in useless_subs:
            if substring in title:
                flag = True
                break
        if not flag:
            processed_titles.append(title[7:-8])

    output_data = tuple(zip(processed_titles, links))
    return output_data


def send_notification(data, bot_token, client_id):
    pass


if __name__ == '__main__':
    import os

    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    load_dotenv()
    get_data()
    send_notification(
        data=get_data(),
        bot_token=os.getenv('BOT_TOKEN', default=''),
        client_id=os.getenv('CLIENT_ID', default='')
    )
