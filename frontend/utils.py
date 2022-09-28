import os
import json


def edit_acc_in_db(key, accounts_details: dict):
    file_name = os.path.join(os.getcwd(), 'files', 'accounts.json')
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    acc_to_edit = [i for i in accounts_list if key in i.values()][0]
    last_tweet = acc_to_edit.get('last_tweet')
    accounts_list.remove(acc_to_edit)
    new_acc_dict = {
        "acc_gmail": accounts_details.get('-gmail-'),
        "acc_pass": accounts_details.get('-pass-'),
        "acc_username": accounts_details.get('-username-'),
        "last_tweet": last_tweet
    }
    accounts_list.append(new_acc_dict)

    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def get_accs_from_db() -> list:
    file_name = os.path.join(os.getcwd(), 'files', 'accounts.json')
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
        accounts_list = (json.loads(data)).get('accounts')
        return accounts_list
    else:
        raise FileNotFoundError('Settings.json file does not exists')


def add_acc_to_db(accounts_details: dict):
    file_name = os.path.join(os.getcwd(), 'files', 'accounts.json')
    new_acc_dict = {
        "acc_gmail": accounts_details.get('-gmail-'),
        "acc_pass": accounts_details.get('-pass-'),
        "acc_username": accounts_details.get('-username-'),
        "last_tweet": None
    }
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    accounts_list.append(new_acc_dict)
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def del_acc_in_db(username_key):
    file_name = os.path.join(os.getcwd(), 'files', 'accounts.json')
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    acc_to_del = [i for i in accounts_list if username_key in i.values()][0]
    accounts_list.remove(acc_to_del)
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def get_current_settings() -> dict:
    file_name = os.path.join(os.getcwd(), 'files', 'settings.json')
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
        setting = (json.loads(data)).get('settings')
        return setting
    else:
        raise FileNotFoundError('Settings.json file does not exists')


def change_current_settings(values: dict):
    file_name = os.path.join(os.getcwd(), 'files', 'settings.json')
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
    file_path = os.path.join(os.getcwd(), 'files', 'tweets.txt')
    mode = 'a'
    if not os.path.exists(file_path):
        mode = 'w'
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(tweet)
        f.write('\n====\n')


def check_file(file_path):  # returns a file object if the file has valid delimiting else return None
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
    file_path = os.path.join(os.getcwd(), 'files', 'tweets.txt')
    with open(file_path, 'a', encoding='utf-8') as f:
        for t in tweets_msgs:
            if t:
                f.write(t)
                f.write('\n====\n')




