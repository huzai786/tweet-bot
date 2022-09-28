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
        quotes.append(quote_text.strip())
    with open('files/quotes.txt', 'w', encoding='utf-8') as f:
        for q in quotes:
            tweet_msg = f'{q}'
            if len(tweet_msg) < 90:
                f.write(tweet_msg)
                f.write('\n')


def use_api_for_quotes():
    ql = []
    while True:
        res = requests.get('https://zenquotes.io/api/random')
        print(res.json())
        if res.json()[0]['q'] != 'Too many requests. Obtain an auth key for unlimited access.':
            quote = res.json()[0]['q']
            ql.append(quote)
        else:
            break

    with open('files/quotes.txt', 'a') as f:
        for q in ql:
            f.write(q)
            f.write('\n')


use_api_for_quotes()
