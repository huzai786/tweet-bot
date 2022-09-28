
    def pick_date(self, date, month, year):
        month_status = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="caltitle"]')))
        _month, _year = (month_status.text).split()
        next_month_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="next-month"]')))
        while True:
            month_status = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="caltitle"]')))
            _month, _year = (month_status.text).split()

            if _month == month:
                break
            next_month_btn.click()
            time.sleep(1)

        next_month_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="next-month"]')))

        while True:
            if year == _year:
                break
            else:
                next_month_btn.click()
                time.sleep(0.5)

        all_active_dates = self.driver.find_elements(
            By.XPATH, f'//*[@id="calweeks"]//a[not(contains(@class,"caldisabled")) or not(contains(@class,"caloff"))]')
        for day in all_active_dates:
            if day.text == date:
                day.click()
                break

        time.sleep(1)

    def schedule_time_function(self, hour, minute, ampm_status):
        action = ActionChains(self.driver)
        self.driver.implicitly_wait(10)
        schedule_tweet_btn = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[13]/button')
        action.scroll_to_element(schedule_tweet_btn)
        action.perform()
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", schedule_tweet_btn)
        schedule_tweet_btn.click()
        schedule_tweet_btn.send_keys(Keys.END)
        schedule_tweet_btn.send_keys(Keys.END)
        self.driver.implicitly_wait(10)
        popver = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div[1]/div[13]/span/div')
        if popver.is_displayed():
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", popver)
            hour_btn = self.driver.find_element(
                By.XPATH, '//*[@id="scheduled-hour"]')
            hour_btn.clear()
            hour_btn.send_keys(Keys.BACKSPACE)
            hour_btn.send_keys(Keys.BACKSPACE)
            hour_btn.send_keys(Keys.BACKSPACE)
            hour_btn.send_keys(hour)
            self.driver.implicitly_wait(10)
            minute_btn = self.driver.find_element(
                By.XPATH, '//*[@id="scheduled-minute"]')
            minute_btn.clear()
            minute_btn.send_keys(minute)
            minute_btn.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(10)
            ampm_btn = self.driver.find_element(By.XPATH, '//*[@id="amPm"]')
            if ampm_btn.text != ampm_status:
                ampm_btn.click()

    def tweet_automation(self, tweets, interval, schedule_till, add_random_emoji, no_of_emoji, add_random_number, add_current_date, add_quotes):
        start_time = datetime.now()
        schedule_till = schedule_till * 30
        end_time = start_time + timedelta(days=schedule_till)
        try:   
            while True:
                if start_time > end_time:
                    break  
                start_time += timedelta(minutes=interval)
                increased_datetime = start_time.strftime(
                    '%#d-%B-%Y-%#I-%M-%p').split('-')
                date, month, year, hour, minute, ampm = increased_datetime
                random_tweet_instance = random.sample(tweets, k=1)[0]
                msg = add_tweet_variables(
                    add_random_emoji, no_of_emoji, add_random_number, add_current_date, add_quotes)
                tweet_msg = f"""{random_tweet_instance.get('tweet')}\n{msg}"""
                if len(tweet_msg) > 265:
                    msg = add_tweet_variables(
                        add_random_emoji, no_of_emoji, add_random_number, add_current_date, False)
                    tweet_msg = f'{random_tweet_instance.get("tweet")}\n{msg}'
                if random_tweet_instance.get('img') != 'No image':
                    send_img_btn = self.driver.find_element(
                        By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/button')
                    if send_img_btn.is_displayed():
                        send_img_btn.click()
                    time.sleep(2)
                    pyautogui.write(random_tweet_instance.get('img'))
                    pyautogui.press('enter')
                self.driver.implicitly_wait(10)
                tweet_box = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[7]/textarea')
                self.driver.execute_script(
                    JS_ADD_TEXT_TO_INPUT, tweet_box, tweet_msg)
                page = self.driver.find_element(
                    By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[3]/div')
                self.schedule_time_function(hour, minute, ampm)
                self.pick_date(date, month, year)
                self.driver.implicitly_wait(10)
                send_tweet_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[12]/div/div/button'))
                )
                if send_tweet_btn.is_enabled():
                    send_tweet_btn.click()
                self.driver.implicitly_wait(10)
                time.sleep(2)
            
        except Exception as e:
            print(e)

