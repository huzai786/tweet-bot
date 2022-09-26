import os

import requests
from bs4 import BeautifulSoup


def dump_quotes_to_html():
    quotes_list = []
    for i in range(1, 11):
        url = f'https://www.azquotes.com/top_quotes.html?p={i}'
        if i == 1:
            url = 'https://www.azquotes.com/top_quotes.html'
        res = requests.get(url)
        bs = BeautifulSoup(res.content, 'lxml')
        quotes_tags = bs.select('ul.list-quotes > li')
        print(url, len(quotes_tags))
        print('===================')
        for q in quotes_tags:
            quotes_list.append(q.prettify())

    print('Dumping quotes')

    with open('quotes.html', 'w', encoding='utf-8') as f:
        for q in quotes_list:
            f.write(q)

def dump_quotes_to_file():
    with open('quotes.html', 'r', encoding='utf-8') as f:
        data = f.read()
    bs = BeautifulSoup(data, 'lxml')
    quotes_lis = bs.find_all('li')
    quotes = []
    for q in quotes_lis:
        quote_text = q.find('a', class_='title').text
        quote_author = q.find('div', class_="author").find('a').text

        quotes.append((quote_text.strip(), quote_author.strip()))
    with open('files/quotes.txt', 'w', encoding='utf-8') as f:
        for quote in quotes:
            tweet_msg = f'"{quote[0]}" -{quote[1]}'
            if len(tweet_msg) < 90:
                f.write(tweet_msg)
                f.write('\n')
    os.unlink('files/quotes.txt')
dump_quotes_to_file()
