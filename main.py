import os
import concurrent.futures
import time

import PySimpleGUI as sg

from frontend.accounts import (
    get_accounts_table,
    add_account_window,
    manage_account_window
)
from frontend.settings import (
    get_setting_table,
    setting_window,
)
from utils import (
    get_current_settings,
    add_to_tweet_file,
    check_file,
    dump_tweets,
    get_accs_from_db
)
from backend.tweet import TweetSchedule
from backend.status import update_status


# Set the theme
sg.theme('DarkAmber')
sg.set_options(font='sans-serif 11')


def main_window():
    settings_heading = ["Settings", "Value"]
    settings = get_setting_table()

    accounts_heading = ["Account Username", "Gmail", "Account Status", "last tweet"]
    accounts = get_accounts_table()

    layout = [
        [sg.Text('Enter Tweets msg:', font=("Arial", 16, 'bold'), tooltip='Enter tweet of length 155'),
         sg.Push(), sg.Button('Close', key='Cancel', size=(10, 1))],
        [sg.Multiline('', autoscroll=True, size=(120, 8), key='tweet_msg')],
        [
            sg.Button('add tweet', key='-add_tweet-'),
            sg.Push(),
            sg.Input(key='-file-', enable_events=True, visible=False),
            sg.FileBrowse('Import from file', file_types=(("Tweet File", "*.txt"),), tooltip='Must have "====" as a delimiter',
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
            sg.Button('Update Status', key='-update_status-'),
            sg.Push(), sg.Button('Start Scheduling', key='-run-', size=(20, 1))
        ],
    ]

    window = sg.Window('Twitter Bot', layout, finalize=True)

    return window


def start_all_accounts_scheduling():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        accounts = get_accs_from_db()
        for a in accounts:
            account = TweetSchedule(a.get('acc_username'), a.get('acc_pass'))
            executor.submit(account.start_scheduling)
            time.sleep(5)

def main():
    window = main_window()
    while True:
        event, value = window.read(timeout=500)
        print(event, value)
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        if event == '-update_status-':
            if sg.popup_ok_cancel('Update Accounts Status?') == 'OK':
                window.perform_long_operation(update_status, '-status-')
                window['-update_status-'].update('Updating..')
                window['-update_status-'].update(disabled=True)
                window['-update_status-'].update(button_color=('black', 'red'))

        if event == '-status-':
            window['-update_status-'].update('Update Status')
            window['-update_status-'].update(button_color=sg.theme_button_color())
            window['-update_status-'].update(disabled=False)
            window.close()
            window = main_window()

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
            tweet = value['tweet_msg']
            if tweet:
                if len(tweet) > 135:
                    sg.popup_error(f'tweet msg len is greater than 135, tweet length = {len(tweet)}')
                    continue
                add_to_tweet_file(tweet)
                window['tweet_msg'].update('')

            else:
                sg.popup_error('Enter Tweet Msg!', modal=True)

        # view tweets
        if event == 'view_raw':
            tweet_file_name = os.path.join(os.getcwd(), 'db', 'tweets.txt')
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

        if event == '-run-':
            msg = sg.popup_ok_cancel('Are you sure you want to start scheduling?')
            if msg == 'OK':
                window.perform_long_operation(start_all_accounts_scheduling, end_key='-DONE_TWEETING-')
                window['-run-'].update('Scheduling...')
                window['-run-'].update(button_color=('black', 'red'))

        if event == '-DONE_TWEETING-':
            window.close()
            window = main_window()
            window['-run-'].update('Start Scheduling')
            window['-run-'].update(button_color=sg.theme_button_color())
            sg.popup_auto_close('Scheduling Completed!')

    window.close()


if __name__ == '__main__':
    main()

