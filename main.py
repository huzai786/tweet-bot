import json
import os
from typing import Any

import PySimpleGUI as sg

# Set the theme
sg.theme('DarkAmber')
sg.set_options(font='sans-serif 11')


# TODO: Selenium and all the rest back-end code


# ------------------settings section start----------------------- #

def get_current_settings() -> dict:
    file_name = os.path.join(os.getcwd(), 'files', 'settings.json')
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()
        setting = (json.loads(data)).get('settings')
        return setting
    else:
        raise FileNotFoundError('Settings.json file does not exists')


def get_setting_table():
    current_settings = get_current_settings()
    settings_tablef: list[list[str | None | Any]] = [
        ["Interval between tweets", current_settings.get('tweet_interval')],
        ["add random emoji's", current_settings.get('random_emoji')],
        ["Number of Emoji's", current_settings.get('no_of_emoji')],
        ["add random characters", current_settings.get('random_char')],
        ["add current data", current_settings.get('curr_date')],
        ["add quotes", current_settings.get('quotes')],
    ]
    return settings_tablef


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
    with open(file_name, 'w', encoding='utf-8') as wf:
        json.dump(data, wf)


def setting_window(settings_dict):
    tweet_interval = [5, 10, 15, 20, 25, 30]
    number_of_emoji = [1, 2, 3, 4, 5, 6]
    setting_layout = [
        [sg.Text('Settings', font=("Arial", 19))],
        [sg.Text('tweet interval'), sg.Push(), sg.OptionMenu(tweet_interval, default_value=settings_dict.get('tweet_interval'),
                                               key='-tweet_interval-')],
        [sg.Text('no of emoji'), sg.Push(), sg.OptionMenu(number_of_emoji, default_value=settings_dict.get('no_of_emoji'),
                                               key='-emoji_no-', tooltip='if random emoji is True')],
        [sg.Text('random emoji'), sg.Push(), sg.Checkbox('', default=settings_dict.get('random_emoji'), key='-emoji-')],
        [sg.Text('add random characters'), sg.Push(), sg.Checkbox('', default=settings_dict.get('random_char'), key='-char-')],
        [sg.Text('add current date'), sg.Push(), sg.Checkbox('', default=settings_dict.get('curr_date'), key='-date-')],
        [sg.Text('add Quotes'), sg.Push(), sg.Checkbox('', default=settings_dict.get('quotes'), key='-quote-')],
        [sg.Button('Save', key='-save-'), sg.Push(), sg.Cancel()]
    ]

    sett_window = sg.Window('Setting', setting_layout)
    while True:
        sett_event, sett_value = sett_window.read()
        print(sett_event, sett_value)
        if sett_event == sg.WINDOW_CLOSED or sett_event == 'Cancel':
            break
        if sett_event == '-save-':
            change_current_settings(sett_value)
            break

    sett_window.close()

# ------------------accounts management start------------------------ #

def edit_acc_in_db(key, accounts_details: dict):
    file_name = os.path.join(os.getcwd(), 'files', 'accounts.json')
    new_acc_dict = {
        "acc_gmail": accounts_details.get('-gmail-'),
        "acc_pass": accounts_details.get('-pass-'),
        "acc_username": accounts_details.get('-username-'),
    }
    with open(file_name, 'r', encoding='utf-8') as rf:
        data = json.load(rf)
    accounts_list = data.get('accounts')
    acc_to_edit = [i for i in accounts_list if key in i.values()][0]
    accounts_list.remove(acc_to_edit)
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
        "acc_username": accounts_details.get('-username-')
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


def get_accounts_table():
    acc_details = get_accs_from_db()
    accounts_table = [[i.get('acc_username'),
                       i.get('acc_gmail'),
                       i.get('acc_status')
                       ] for i in acc_details]
    return accounts_table


def get_manage_window():
    accs = get_accs_from_db()  # Lists of all the accounts in db
    manage_acc_layout = [
        [
            sg.Text(f'{i.get("acc_gmail")}'),
            sg.Text(f'{i.get("acc_username")}'),
            sg.Push(),
            sg.Button('Edit', key=f'{i.get("acc_username") + "_edit"}'),
            sg.Button('Delete', key=f'{i.get("acc_username") + "_delete"}')
        ]
        for i in accs  # List Comprehension
    ]
    w = sg.Window('Manage Accounts', manage_acc_layout)

    return w


def manage_account_window():
    """Handles the Edit and Delete Button"""

    manage_acc_window = get_manage_window()

    while True:
        manage_acc_event, eod_acc_value = manage_acc_window.read()
        print(manage_acc_event, eod_acc_value)
        if manage_acc_event == sg.WINDOW_CLOSED or manage_acc_event == 'Cancel':
            break

        key = manage_acc_event.split('_')[0]

        if manage_acc_event.endswith('_edit'):
            edit_account_window(key)
            manage_acc_window.close()
            manage_acc_window = get_manage_window()

        if manage_acc_event.endswith('_delete'):
            if sg.popup_yes_no(f'Are you sure you want to delete {key} account!', keep_on_top=True, modal=True) == 'Yes':
                del_acc_in_db(key)
                manage_acc_window.close()
                manage_acc_window = get_manage_window()

    manage_acc_window.close()


def edit_account_window(key):
    accs = get_accs_from_db()  # Lists of all accounts dict

    x = [i for i in accs if key in i.values()][0]

    username = x.get("acc_username")
    gmail = x.get('acc_gmail')
    password = x.get('acc_pass')

    edit_account_layout = [
        [sg.Text('Account username:'), sg.InputText(username, key='-username-')],
        [sg.Text('Account gmail:        '), sg.InputText(gmail, key='-gmail-')],
        [sg.Text('Account password: '), sg.InputText(password, key='-pass-')],
        [sg.Button('Save', key='-save-'), sg.Cancel()]
    ]
    edit_acc_window = sg.Window('Edit Account', edit_account_layout)

    while True:
        edit_acc_event, edit_acc_value = edit_acc_window.read()

        if edit_acc_event == sg.WINDOW_CLOSED or edit_acc_event == 'Cancel':
            break

        if edit_acc_event == '-save-':
            if edit_acc_value.get('-username-') and edit_acc_value.get('-gmail-') and edit_acc_value.get('-pass-'):
                edit_acc_in_db(key, edit_acc_value)

            else:
                sg.popup_error('Value Missing!', modal=True)
                continue

            break

    edit_acc_window.close()


def add_account_window():
    add_account_layout = [
        [sg.Text('Account username:'), sg.InputText(key='-username-')],
        [sg.Text('Account gmail:        '), sg.InputText(key='-gmail-')],
        [sg.Text('Account password: '), sg.InputText(key='-pass-')],
        [sg.Button('Save', key='-save-'), sg.Cancel()]
    ]
    add_acc_window = sg.Window('Add Account', add_account_layout)

    while True:
        add_acc_event, add_acc_value = add_acc_window.read()
        if add_acc_event == sg.WINDOW_CLOSED or add_acc_event == 'Cancel':
            break

        if add_acc_event == '-save-':
            if add_acc_value.get('-username-') and add_acc_value.get('-gmail-') and add_acc_value.get('-pass-'):
                add_acc_to_db(add_acc_value)

            else:
                sg.popup_error('Value Missing!', modal=True)
                continue

            break

    add_acc_window.close()


# ------------------------- Tweet management Section ------------------#

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

# ----------------------------Main loop--------------------------------#

settings_heading = ["Settings", "Value"]
settings = get_setting_table()

accounts_heading = ["Account Username", "Gmail", "Account Status"]
accounts = get_accounts_table()

layout = [
    [sg.Text('Enter Tweets msg:', font=("Arial", 16, 'bold')), sg.Push(), sg.Button('Close', key='Cancel', size=(10, 1))],
    [sg.Multiline('', autoscroll=True, size=(100, 8), key='tweet_msg')],
    [
        sg.Button('add tweet', key='-add_tweet-'),
        sg.Push(),
        sg.Input(key='-file-', enable_events=True, visible=False),
        sg.FileBrowse('Import from file', file_types=(("Tweet File", "*.txt"),), tooltip='Must have "===" as a delimiter',
                      target='-file-'),
        sg.Button('view tweets', key='view_raw')
    ],
    [sg.Text('Settings:', font=("Arial", 16, 'bold'))],
    [
        sg.Table(settings, headings=settings_heading, justification='left', key='-setting_table-'),
        sg.Push(),
        sg.Table(accounts, headings=accounts_heading, justification='left', key='-acc_table-')
    ],
    [
        sg.Button('Edit Configuration', key='-edit_config-'),
        sg.Button('Add Accounts', key='-add_acc-'),
        sg.Button('Manage Accounts', key='-manage_acc-'),
        sg.Push(), sg.Button('Run Bot', key='-run-', size=(20, 1))
    ],
]

window = sg.Window('Twitter Bot', layout, finalize=True)


if __name__ == '__main__':
    while True:
        event, value = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        # Setting configuration
        if event == "-edit_config-":
            setting_window(get_current_settings())
            updated_settings_table = get_setting_table()
            window['-setting_table-'].update(values=updated_settings_table)

        # add accounts
        if event == '-add_acc-':
            add_account_window()
            updated_acc_table = get_accounts_table()
            window['-acc_table-'].update(updated_acc_table)

        # add tweets
        if event == '-add_tweet-':
            if value['tweet_msg']:
                add_to_tweet_file(value['tweet_msg'])
                window['tweet_msg'].update('')

            else:
                sg.popup_error('Enter Tweet Msg!', modal=True)

        # view tweets
        if event == 'view_raw':
            tweet_file_name = os.path.join(os.getcwd(), 'files', 'tweets.txt')
            os.startfile(tweet_file_name)

        # add tweets from file
        if event == '-file-':
            tweets = check_file(value['-file-'])
            if tweets:
                dump_tweets(tweets)

            else:
                sg.popup_error('Delimiter "====" not Found in the File!', modal=True)

        # Accounts Edit and delete
        if event == '-manage_acc-':
            manage_account_window()
            updated_acc_table = get_accounts_table()
            window['-acc_table-'].update(updated_acc_table)

    window.close()

