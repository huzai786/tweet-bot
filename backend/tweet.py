import os
import time
from datetime import datetime, timedelta
from collections import namedtuple
from typing import Union

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from frontend.utils import get_current_settings
from backend.helpers import _side_panel_setup, check_exists
from backend.utils import generate_tweet, _set_options, _extract_time, JS_ADD_TEXT_TO_INPUT


class TweetSchedule:
    options = _set_options()
    settings = get_current_settings()

    def __init__(self, username, password, gmail=None):
        self.username = username
        self.password = password
        self.gmail = gmail
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)

    def go_to_main_page(self, status=False) -> Union[None, str]:
        self.driver.get('https://tweetdeck.twitter.com/')

        login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//section[@data-auth-type='twitter']/div/a")))
        login.click()

        username = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text'][@autocapitalize='sentences']")))
        username.send_keys(self.username)
        username.send_keys(Keys.ENTER)

        password = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password'][@type='password']")))
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(15)
        if status:
            if check_exists(self.driver, By.XPATH, '//head/meta[@content="TweetDeck"]'):
                return 'Active'
            else:
                return 'Phone Verification Requires'

    def last_tweet_time(self, tweet_time=None, dump=False) -> datetime:
        """Will either return the datetime of last tweet of current time if tweet is scheduled or doesn't exist"""
        file_name = os.path.join(os.getcwd(), 'files', 'settings.json')

        with open(file_name, 'r') as f:
            data = f.readlines()
            if data:
                time_str = data[0].strip('\n')
                return datetime.strptime(time_str, '%I:%M %p %a %d %B %Y')
            else:
                open(file_name, 'w')

        if dump and tweet_time:
            with open(file_name, 'w') as f:
                f.write(tweet_time.strftime('%I:%M %p %a %d %B %Y'))


        scheduled_section = self.driver.find_element(By.XPATH,
                                                     '//div/header/div/div/span[text()="Scheduled"]/../../../..')
        try:
            scheduled_tweets = scheduled_section.find_elements(By.XPATH, './/article')
            print([i.text for i in scheduled_tweets])
            date_string = scheduled_tweets[-1].find_element(By.XPATH, './/span').text
            date = datetime.strptime(date_string, '%I:%M %p · %a %d %B %Y')

            return date

        except NoSuchElementException:
            return datetime.now()

        except IndexError:
            return datetime.now()

    def page_setup(self) -> None:
        _side_panel_setup(self.driver)
        stay_open = self.driver.find_element(By.XPATH, '//footer/label/input[@type="checkbox"]')
        if not stay_open.is_selected():
            stay_open.click()

    def _pick_date(self, date, month, year):

        current_month, current_year = self.driver.find_element(By.XPATH, '//*[@id="calhead"]').text.split()

        while current_month != month or current_year != year:

            next_month_button = self.driver.find_element(By.XPATH, '//*[@id="next-month"]')
            next_month_button.click()

            current_month, current_year = self.driver.find_element(By.XPATH, '//*[@id="calhead"]').text.split()

        active_dates = self.driver.find_elements(By.XPATH,
                    '//div[@id="calweeks"]//a[not(contains(@class,"caldisabled")) and not(contains(@class,"caloff"))]')

        for d in active_dates:
            if d.text == date:
                d.click()
                break

    def _pick_time(self, hour, minute, ampm):
        hour_input = self.driver.find_element(By.XPATH, '//*[@id="scheduled-hour"]')
        minute_input = self.driver.find_element(By.XPATH, '//*[@id="scheduled-minute"]')

        hour_input.clear()
        hour_input.send_keys(hour)
        hour_input.send_keys(Keys.ENTER)

        minute_input.clear()
        minute_input.send_keys(minute)
        minute_input.send_keys(Keys.ENTER)

        ampm_status = self.driver.find_element(By.XPATH, '//*[@id="amPm"]')
        if not ampm_status.text == ampm:
            ampm_status.click()

    def schedule(self, time_to_schedule: namedtuple) -> None:
        self.driver.find_element(By.XPATH, '//div[@class="js-scheduler"]/button').click()
        calendar = self.driver.find_element(
            By.XPATH, '//span[@class="js-schedule-datepicker-holder"]/div')

        if calendar.is_displayed():
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", calendar)

        self._pick_date(time_to_schedule.date, time_to_schedule.month, time_to_schedule.year)
        self._pick_time(time_to_schedule.hour, time_to_schedule.minute, time_to_schedule.ampm)
        self.driver.implicitly_wait(10)

    def write_tweet(self) -> None:
        tweet_msg = generate_tweet(self.settings)
        tweet_box = self.driver.find_element(By.XPATH, '//textarea[@placeholder="What\'s happening?"]')
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, tweet_box, tweet_msg)
        time.sleep(1)

    def post_tweet(self) -> None:

        schedule_tweet_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                '//div[@class="pull-right"]/div/button[@data-original-title="Tweet (Ctrl+Enter)"]')))
        if schedule_tweet_button.is_enabled():
            schedule_tweet_button.click()
        self.driver.implicitly_wait(10)
        time.sleep(1.5)

    def start_scheduling(self, schedule_till=settings.get('schedule_till')):
        """Schedule tweet till a specific time and returns the last tweet posting time"""

        self.go_to_main_page()
        self.page_setup()

        scheduling_start_time = self.last_tweet_time()
        scheduling_end_time = scheduling_start_time + timedelta(days=int(schedule_till))
        interval = int(self.settings.get('tweet_interval'))
        print('scheduling_start_time', scheduling_start_time)
        while scheduling_start_time < scheduling_end_time:

            schedule_time = scheduling_start_time + timedelta(minutes=interval)
            schedule_time_values = _extract_time(schedule_time)

            print(scheduling_start_time)

            self.schedule(schedule_time_values)
            self.write_tweet()
            self.post_tweet()

            scheduling_start_time += timedelta(minutes=interval)

        self.driver.quit()
        self.last_tweet_time(dump=True, tweet_time=scheduling_start_time)
