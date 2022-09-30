import concurrent.futures
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from utils import get_accs_from_db, edit_acc_in_db
from backend.tweet import TweetSchedule

def _get_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, '%m/%d/%Y, %H:%M')


def open_account(account: dict) -> str:
    acc = TweetSchedule(account.get('acc_username'), account.get('acc_pass'))
    status = acc.go_to_main_page(status=True)
    return status

def update_status():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        accounts = get_accs_from_db()
        future = [executor.submit(open_account, a) for a in accounts]

    statuses = [(f.result(), a.get('acc_username')) for f, a in zip(future, accounts)]

    for st in statuses:
        acc = [i for i in accounts if i.get('acc_username') == st[0]][0]
        acc['status'] = st[1]
        edit_acc_in_db(acc['acc_username'], acc)
