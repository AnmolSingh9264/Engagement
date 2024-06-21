import pickle
import time
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
import controller
import selenium.common.exceptions
from selenium import webdriver
import os
import chromedriver_autoinstaller as chromedriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from flask import Flask, request

app = Flask(__name__)
path = str(os.path.dirname(os.path.abspath(__file__)))
print(path)
driver = None
optionss = Options()
try:
    driver = webdriver.Chrome(service=Service(executable_path=path+'/126/chromedriver.exe'), options=optionss)
except FileNotFoundError:
    chromedriver.install(path=path)
    driver = webdriver.Chrome(service=Service(executable_path=path + '/126/chromedriver.exe'), options=optionss)
except selenium.common.WebDriverException:
    print("chrome driver exception")
    chromedriver.install(path=path)
    driver = webdriver.Chrome(service=Service(executable_path=path+/126/chromedriver.exe'), options=optionss)

optionss.add_argument('--headless')
def login(id, password):
    controller.auth(id, driver, "text")
    controller.login(driver, "//*[contains(text(), 'Next')]")
    controller.auth(password, driver, "password")
    controller.login(driver, "//span[contains(text(), 'Log in')]")


driver.get("https://twitter.com/login?lang=en")
for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'html'))):
    file = open(path+'/accounts.txt', 'r')
    try:
        with open(path + "/cookies.pkl", "rb") as file:
            pass
    except FileNotFoundError:
        login(file.readline().strip(), file.readline().strip())

for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'html'))):

    try:
        with open(path+"/cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get("https://twitter.com/home")
    except FileNotFoundError:
        time.sleep(60)
        cookies = driver.get_cookies()
        with open(path+"/cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
        with open(path+"/cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get("https://twitter.com/home")

@app.route('/geturl')
def getUrl():
    return str(driver.current_url)

@app.route('/view')
def openNewTab():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(request.args.get('url'))
    html = driver.find_element(By.TAG_NAME, 'html')
    try:
        for button in WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-testid=\"retweet\"]"))):
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
            html.send_keys(keys.Keys.PAGE_DOWN)
            time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except selenium.common.exceptions.ElementClickInterceptedException:
        print("Click intercepted")
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Stale element")
    except selenium.common.TimeoutException:
        print("timeout2")
    except selenium.common.NoSuchElementException:
        print("element not found")
        html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotVisibleException:
        print("element not visible")
        html.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotInteractableException:
        print("element not interceptable")
    return "True"


@app.route('/retweet')
def retweet():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(request.args.get('url'))
    html = driver.find_element(By.TAG_NAME, 'html')
    try:
        while True:
            button = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"retweet\"]")))
            button.click()
            controller.login(driver, "//*[text()='Repost']")
            break
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except selenium.common.exceptions.ElementClickInterceptedException:
        print("Click intercepted")
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Stale element")
    except selenium.common.TimeoutException:
        print("timeout2")
    except selenium.common.NoSuchElementException:
        print("element not found")
        html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotVisibleException:
        print("element not visible")
        html.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotInteractableException:
        print("element not interceptable")
    return "Reposted Successfully"

@app.route('/like')
def like():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(request.args.get('url'))
    html = driver.find_element(By.TAG_NAME, 'html')
    try:
        while True:
            button = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"like\"]")))
            button.click()
            break
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except selenium.common.exceptions.ElementClickInterceptedException:
        print("Click intercepted")
    except selenium.common.exceptions.StaleElementReferenceException:
        print("Stale element")
    except selenium.common.TimeoutException:
        print("timeout2")
    except selenium.common.NoSuchElementException:
        print("element not found")
        html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotVisibleException:
        print("element not visible")
        html.send_keys(keys.Keys.PAGE_DOWN)
    except selenium.common.ElementNotInteractableException:
        print("element not interceptable")
    return "liked successfully"

@app.route('/comment')
def comment():
    commentdriver = driver
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(request.args.get('url'))
    html = driver.find_element(By.TAG_NAME, 'html')
    while True:
        try:
            button = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"tweetTextarea_0\"]")))
            button.send_keys(request.args.get('msg'))
            controller.login(driver, "//*[text()='Reply']")
            time.sleep(5)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            break
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("Click intercepted")
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale element")
        except selenium.common.TimeoutException:
            print("timeout2")
        except selenium.common.NoSuchElementException:
            print("element not found")
            html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotVisibleException:
            print("element not visible")
            html.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotInteractableException:
            print("element not interceptable")
            html.send_keys(keys.Keys.PAGE_DOWN)
    return "commented successfully"


@app.route('/all')
def allAction():
    alldriver = driver
    alldriver.execute_script("window.open('');")
    alldriver.switch_to.window(alldriver.window_handles[1])
    alldriver.get(request.args.get('url'))
    html = alldriver.find_element(By.TAG_NAME, 'html')
    while True:
        try:
            if request.args.get('r') is not None:
                button = WebDriverWait(alldriver, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"retweet\"]")))
                button.click()
                controller.login(alldriver, "//*[text()='Repost']")
            if request.args.get('l') is not None:
                button = WebDriverWait(alldriver, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"like\"]")))
                button.click()
            if request.args.get('msg') is not None:
                button = WebDriverWait(alldriver, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"tweetTextarea_0\"]")))
                button.send_keys(request.args.get('msg'))
                controller.login(alldriver, "//*[text()='Reply']")
                time.sleep(5)
            alldriver.close()
            alldriver.switch_to.window(driver.window_handles[0])
            break
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("Click intercepted")
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale element")
        except selenium.common.TimeoutException:
            print("timeout2")
        except selenium.common.NoSuchElementException:
            print("element not found")
            html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotVisibleException:
            print("element not visible")
            html.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotInteractableException:
            print("element not interceptable")
            html.send_keys(keys.Keys.PAGE_DOWN)
    return "Action Completed successfully"

@app.route('/test')
def test():
    alldriver = driver
    alldriver.execute_script("window.open('');")
    alldriver.switch_to.window(alldriver.window_handles[1])
    alldriver.get(request.args.get('url'))
    html = alldriver.find_element(By.TAG_NAME, 'html')
    alldriver.close()
    alldriver.switch_to.window(driver.window_handles[0])
    return "opened"


@app.route('/post')
def post():
    html = driver.find_element(By.TAG_NAME, 'html')
    while True:
        try:
            button = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid=\"tweetTextarea_0\"]")))
            button.send_keys(request.args.get('msg'))
            controller.login(driver, "//*[text()='Post']")
            time.sleep(5)
            break
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("Click intercepted")
        except selenium.common.exceptions.StaleElementReferenceException:
            print("Stale element")
        except selenium.common.TimeoutException:
            print("timeout2")
        except selenium.common.NoSuchElementException:
            print("element not found")
            html.send_keys(keys.Keys.PAGE_DOWN)
        # if retbtn != None:
        # retbtn.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotVisibleException:
            print("element not visible")
            html.send_keys(keys.Keys.PAGE_DOWN)
        except selenium.common.ElementNotInteractableException:
            print("element not interceptable")
            html.send_keys(keys.Keys.PAGE_DOWN)
    return "Posted successfully"


@app.route('/refresh')
def refresh():
    driver.refresh()
    return "Refreshed successfully: "+driver.current_url

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9708)
