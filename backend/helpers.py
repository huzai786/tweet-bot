from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def check_exists(driver, method, selector):
    try:
        driver.find_element(method, selector)
        
    except NoSuchElementException:
        return False
    return True


def _side_panel_setup(driver):
    side_panel_closed_xpath = 'html > body > div > header > div > button[data-drawer="compose"]'
    if not check_exists(driver, By.CSS_SELECTOR, 'div.js-account-list > div > a'):
        side_panel_closed = driver.find_element(By.CSS_SELECTOR, side_panel_closed_xpath)
        side_panel_closed.click()

