from typing import Any
import PySimpleGUI as sg

from frontend.utils import get_current_settings, change_current_settings


def get_setting_table():
    current_settings = get_current_settings()
    settings_tablef: list[list[str | None | Any]] = [
        ["Interval between tweets", current_settings.get('tweet_interval')],
        ["add random emoji's", current_settings.get('random_emoji')],
        ["Number of Emoji's", current_settings.get('no_of_emoji')],
        ["add random characters", current_settings.get('random_char')],
        ["add current data", current_settings.get('curr_date')],
        ["add quotes", current_settings.get('quotes')],
        ["Schedule Till (days)", current_settings.get('schedule_till')],
    ]
    return settings_tablef


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
        [sg.Text('Schedule till (days)'), sg.Push(), sg.Input(settings_dict.get('schedule_till'), key='-schedule_till-', size=(10, 1))],
        [sg.Button('Save', key='-save-'), sg.Push(), sg.Cancel()]
    ]

    sett_window = sg.Window('Setting', setting_layout)
    while True:
        sett_event, sett_value = sett_window.read()
        print(sett_event, sett_value)
        if sett_event == sg.WINDOW_CLOSED or sett_event == 'Cancel':
            break
        if sett_event == '-save-':
            try:
                int(sett_value.get('-schedule_till-'))
                change_current_settings(sett_value)
                break
            except ValueError:
                sg.popup_error('pass integer value to field "schedule till"')
                continue

    sett_window.close()
