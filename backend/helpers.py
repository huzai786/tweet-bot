from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def check_exists(driver, method, selector):
    try:
        driver.find_element(method, selector)
        
    except NoSuchElementException:
        return False
    return True


def _side_panel_setup(driver):
    side_panel_closed_xpath = 'html > body > div > header > div > button[data-drawer="compose"]'
    if not check_exists(driver, By.CSS_SELECTOR, 'div.js-account-list > div > a'):
        side_panel_closed = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, side_panel_closed_xpath)))
        side_panel_closed.click()



