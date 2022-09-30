import PySimpleGUI as sg

from utils import (
    get_accs_from_db,
    del_acc_in_db,
    edit_acc_in_db,
    add_acc_to_db
)


def get_accounts_table():

    acc_details = get_accs_from_db()
    accounts_table = [[i.get('acc_username'),
                       i.get('acc_gmail'),
                       i.get('status'),
                       i.get('last_tweet')
                       ] for i in acc_details]

    return accounts_table


def get_manage_window(accounts):

    manage_acc_layout = [
        [
            sg.Text(f'{i.get("acc_gmail")}'),
            sg.Text(f'{i.get("acc_username")}'),
            sg.Push(),
            sg.Button('Edit', key=f'{i.get("key")}-edit'),
            sg.Button('Delete', key=f'{i.get("key")}-delete')
        ]
        for i in accounts  # List Comprehension
    ]
    w = sg.Window('Manage Accounts', manage_acc_layout)

    return w


def manage_account_window():
    """Handles the Edit and Delete Button"""
    accs = get_accs_from_db()

    manage_acc_window = get_manage_window(accs)

    if not accs:
        sg.popup_error('No Account Found To Manage!')
        manage_acc_window.close()

    while True:
        manage_acc_event, eod_acc_value = manage_acc_window.read()
        if manage_acc_event == sg.WINDOW_CLOSED or manage_acc_event == 'Cancel':
            break

        key = manage_acc_event.split('-')[0]

        if manage_acc_event.endswith('edit'):
            edit_account_window(key)
            manage_acc_window.close()
            accs = get_accs_from_db()
            manage_acc_window = get_manage_window(accs)

        if manage_acc_event.endswith('delete'):
            if sg.popup_yes_no(f'Are you sure you want to delete account!', keep_on_top=True, modal=True) == 'Yes':
                del_acc_in_db(key)
                manage_acc_window.close()
                accs = get_accs_from_db()
                if accs:
                    manage_acc_window = get_manage_window(accs)
                else:
                    manage_acc_window.close()

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
                things_to_edit = {
                    "acc_username": edit_acc_value.get('-username-'),
                    "acc_gmail": edit_acc_value.get('-gmail-'),
                    "acc_pass": edit_acc_value.get('-pass-'),
                }
                edit_acc_in_db(key, things_to_edit)

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
