def get_raw_data():
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
    return output_data[:5]


def process_data(raw_data):
    title = raw_data[0][0]
    link = raw_data[0][1]
    return f'{title}\n{link}'


def send_notification(processed_data, tg_context):
    bot = Bot(token=tg_context['bot_token'])
    return bot.send_message(tg_context['client_id'], processed_data)


def main(tg_data):
    while True:
        try:
            raw_data = get_raw_data()
            processed_data = process_data(raw_data)
            send_notification(processed_data, tg_data)
        except Exception:
            msg = 'We have some problems.'
            send_notification(msg, tg_data)
        while raw_data == get_raw_data():
            send_notification(
                'No news right now, wait for 30 minutes to check',
                tg_data
            )
            sleep(30 * 60)


if __name__ == '__main__':
    import os
    from time import sleep

    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    from telegram import Bot
    load_dotenv()
    tg_data = {
        'bot_token': os.getenv('BOT_TOKEN', default='your_precious_token'),
        'client_id': os.getenv('CLIENT_ID', default='your_precious_id')
    }
    main(tg_data)
