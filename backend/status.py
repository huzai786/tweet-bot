import concurrent.futures
import time
from datetime import datetime

from utils import get_accs_from_db
from backend.tweet import TweetSchedule

def _get_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, '%m/%d/%Y, %H:%M')


def open_account(account: dict):
    acc = TweetSchedule(account.get('acc_username'), account.get('acc_pass'))
    acc.go_to_main_page(check_status=True)

def update_status():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        accounts = get_accs_from_db()
        for a in accounts:
            executor.submit(open_account, a)
            time.sleep(2)
