from datetime import datetime, timedelta
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from frontend.utils import get_current_settings
from backend.helpers import side_panel_setup
from backend.utils import generate_tweet, _set_options, _extract_time, JS_ADD_TEXT_TO_INPUT


class TweetSchedule:
    options = _set_options()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    settings = get_current_settings()

    def __init__(self, username, password, gmail=None):
        self.username = username
        self.password = password
        self.gmail = gmail

    def go_to_main_page(self) -> None:
        self.driver.get('https://tweetdeck.twitter.com/')
        login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//section[@data-auth-type='twitter']/div/a")))
        login.click()
        username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text'][@autocapitalize='sentences']")))
        username.send_keys(self.username)
        username.send_keys(Keys.ENTER)

        password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password'][@type='password']")))
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(10)

    def last_tweet_time(self, exit_driver=False) -> datetime:
        """Will either return the datetime of last tweet of current time if tweet is scheduled or doesn't exist"""
        scheduled_section = self.driver.find_element(By.XPATH,
                                                     '//div/header/div/div/span[text()="Scheduled"]/../../../..')
        try:
            scheduled_tweets = scheduled_section.find_element(By.XPATH, './/article')
            date_string = scheduled_tweets.find_element(By.XPATH, './/span').text
            date = datetime.strptime(date_string, '%I:%M %p · %a %d %B %Y')
            if exit_driver:
                self.driver.quit()

            return date

        except NoSuchElementException:
            return datetime.now()

    def page_setup(self) -> None:
        side_panel_setup(self.driver)
        stay_open = self.driver.find_element(By.XPATH, '//footer/label/input[@type="checkbox"]')
        if not stay_open.is_selected():
            stay_open.click()

    def _pick_date(self, date, month, year):
        pass

    def _pick_time(self, hour, minute, ampm):
        pass

    def schedule(self, time_to_schedule: namedtuple) -> None:
        schedule_tweet = self.driver.find_element(By.XPATH, '//div[@class="js-scheduler"]/button')
        schedule_tweet.click()
        self._pick_date(time_to_schedule.date, time_to_schedule.month, time_to_schedule.year)
        self._pick_time(time_to_schedule.hour, time_to_schedule.minute, time_to_schedule.ampm)

    def write_tweet(self) -> None:
        tweet_msg = generate_tweet(self.settings)
        tweet_box = self.driver.find_element(By.XPATH, '')  # incomplete
        tweet_box.send_keys(tweet_msg)

    def post_tweet(self) -> None:
        schedule_tweet_button = self.driver.find_element(By.XPATH, '')  # incomplete
        schedule_tweet_button.click()
        self.driver.implicitly_wait(10)

    def start_scheduling(self, schedule_till=settings.get('schedule_till')) -> namedtuple:
        """Schedule tweet till a specific time and returns the last tweet posting time"""

        self.go_to_main_page()
        self.page_setup()

        scheduling_start_time = self.last_tweet_time()
        scheduling_end_time = scheduling_start_time + timedelta(days=int(schedule_till))

        while scheduling_start_time < scheduling_end_time:

            interval = int(self.settings.get('tweet_interval'))
            schedule_time = scheduling_start_time + timedelta(minutes=interval)
            schedule_time_values = _extract_time(schedule_time)

            self.write_tweet()
            self.schedule(schedule_time_values)  # Opens tweet schedule and handle scheduling
            self.post_tweet()

            scheduling_start_time += timedelta(minutes=interval)

        return _extract_time(scheduling_end_time)
