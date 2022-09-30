import os
import json
import random
import string
from datetime import datetime
from collections import namedtuple

from selenium.webdriver import ChromeOptions


# ------------------ functions for generating tweet msg ------------------ #

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
    file_path = os.path.join(os.getcwd(), 'db', 'tweets.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        all_tweets = f.read()
        tweet_lists = all_tweets.split('====')
        tweet_lists = [i.strip('\n') for i in tweet_lists if i != '\n']
        tweet = random.choice(tweet_lists)
        return tweet.strip('\n')


def get_random_quote() -> str:
    file_path = os.path.join(os.getcwd(), 'db', 'quotes.txt')
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

# --------------------- end ------------------------ #

# -------------------- tweet scheduling utils ----------------------- #
def _set_options() -> ChromeOptions:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    options = ChromeOptions()
    options.add_argument('--headless')
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

# ------------- end ------------- #

# -------------------- account crud -------------------- #

def edit_acc_in_db(key, things_to_edit: dict):
    file_name = os.path.join(os.getcwd(), 'db', 'accounts.json')
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    acc_to_edit = [i for i in accounts_list if key in i.values()][0]
    for i, v in things_to_edit.items():
        acc_to_edit[i] = v
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def get_accs_from_db() -> list:
    file_name = os.path.join(os.getcwd(), 'db', 'accounts.json')
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
        accounts_list = (json.loads(data)).get('accounts')
        return accounts_list
    else:
        raise FileNotFoundError('Settings.json file does not exists')


def add_acc_to_db(accounts_details: dict):
    file_name = os.path.join(os.getcwd(), 'db', 'accounts.json')
    new_acc_dict = {
        "acc_gmail": accounts_details.get('-gmail-'),
        "acc_pass": accounts_details.get('-pass-'),
        "acc_username": accounts_details.get('-username-'),
        "last_tweet": None,
        "status": None,
        "key": ''.join([str(random.randint(0, 10)) for _ in range(4)])
    }

    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    accounts_list.append(new_acc_dict)
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def del_acc_in_db(key):
    file_name = os.path.join(os.getcwd(), 'db', 'accounts.json')
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    acc_to_del = [i for i in accounts_list if key in i.values()][0]
    accounts_list.remove(acc_to_del)
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


# ----------------- Front end utils ---------------- #

def get_current_settings() -> dict:
    file_name = os.path.join(os.getcwd(), 'db', 'settings.json')
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
        setting = (json.loads(data)).get('settings')
        return setting
    else:
        raise FileNotFoundError('Settings.json file does not exists')


def change_current_settings(values: dict):
    file_name = os.path.join(os.getcwd(), 'db', 'settings.json')
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    setting = data.get('settings')
    setting['tweet_interval'] = values.get('-tweet_interval-')
    setting['random_emoji'] = values.get('-emoji-')
    setting['no_of_emoji'] = values.get('-emoji_no-')
    setting['random_char'] = values.get('-char-')
    setting['curr_date'] = values.get('-date-')
    setting['quotes'] = values.get('-quote-')
    setting['schedule_till'] = values.get('-schedule_till-')
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)

def add_to_tweet_file(tweet):
    file_path = os.path.join(os.getcwd(), 'db', 'tweets.txt')
    mode = 'a'
    if not os.path.exists(file_path):
        mode = 'w'
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(tweet)
        f.write('\n====\n')


def check_file(file_path):
    """returns a file object if the file has valid delimiting else return None"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
    tweet_list = []
    _tweets = data.split('====')
    if len(_tweets) > 1:
        for tweet in _tweets:
            t = tweet.strip('\n')
            tweet_list.append(t)

    return tweet_list


def dump_tweets(tweets_msgs: list):
    file_path = os.path.join(os.getcwd(), 'db', 'tweets.txt')
    with open(file_path, 'a', encoding='utf-8') as f:
        for t in tweets_msgs:
            if t:
                f.write(t)
                f.write('\n====\n')




