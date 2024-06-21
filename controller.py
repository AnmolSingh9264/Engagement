from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def auth(value, driver, path):
    for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.NAME, path))):
        button.send_keys(value)


def login(driver, path):
    for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, path))):
        button.click()


def tweet(driver, path, keys):
    for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, path))):
        button.send_keys(keys)
