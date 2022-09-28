import os
import random
import string
from datetime import datetime
from collections import namedtuple

from selenium.webdriver import ChromeOptions


def get_cur_date() -> str:
    now = datetime.now()
    curr_time = now.strftime('%m/%d/%Y, %H:%M')
    return curr_time


def string_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_emoji(length) -> str:
    l = ['😀', '😁', '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍', '😘', '😗', '🤔', '🤫', '🤭', '🤗']
    text = random.sample(l, k=length)

    return ''.join(text)


def get_random_tweet() -> str:
    file_path = os.path.join(os.getcwd(), 'files', 'tweets.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        all_tweets = f.read()
        tweet_lists = all_tweets.split('====')
        tweet_lists = [i.strip('\n') for i in tweet_lists if i != '\n']
        tweet = random.choice(tweet_lists)
        return tweet.strip('\n')


def get_random_quote() -> str:
    file_path = os.path.join(os.getcwd(), 'files', 'quotes.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        l = f.readlines()
    return random.choice(l)


def generate_tweet(settings: dict) -> str:
    tweet = get_random_tweet()
    date = get_cur_date() if settings.get('curr_date') else None
    random_char = string_generator() if settings.get('random_char') else None
    random_emoji = get_random_emoji(int(settings.get('no_of_emoji'))) if settings.get('random_emoji') else None
    quote = get_random_quote()
    content = [tweet, date, random_emoji, random_char, quote]
    tweet_msg = '\n'.join([i for i in content if i])

    return tweet_msg


def _set_options() -> ChromeOptions:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    options = ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(f'--user-agent={ua}')
    return options


def _extract_time(time_obj: datetime) -> namedtuple:
    t = namedtuple('Time', ['month', 'year', 'date', 'hour', 'minute', 'ampm'])

    only_date, only_time = time_obj.date(), time_obj.time()
    only_date_str, only_time_str = only_date.strftime('%Y %B %#d'), only_time.strftime('%#I %M %p')
    year, month, date = only_date_str.split()
    hour, minute, amPm = only_time_str.split()

    values = t(year=year, month=month, date=date, hour=hour, minute=minute, ampm=amPm)
    return values


JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """
