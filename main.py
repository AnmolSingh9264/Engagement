import asyncio
import pickle
import time
from flask import Flask, request
from threading import Thread
from playwright.async_api import async_playwright
import random

app = Flask(__name__)
url = ""
Post = None
tweetUrl = None
retweet = None
like = None
comment = None

useragent = ["Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
             "Mozilla/5.0 (Linux; Android 12; moto g pure) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
             "Mozilla/5.0 (Linux; Android 12; moto g stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36v",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
             "Mozilla/5.0 (Linux; Android 12; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"]

def load_cookies_from_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        cookies = pickle.load(f)
    return cookies


async def run(playwright):
    global url
    global tweetUrl
    global retweet
    global like
    global comment
    global Post
    browser = await playwright.chromium.launch(headless=True,
    args = [
        '--disable-gpu',  # Disable GPU to save resources
        '--no-sandbox',  # No sandbox mode for faster launch
        '--disable-dev-shm-usage'  # Overcome limited resource problems
    ]
    )
    context = await browser.new_context(user_agent= useragent[random.randint(0, 4)])
    context.set_default_timeout(120000)
    page = await context.new_page()
    await page.goto('https://twitter.com')

    await page.wait_for_load_state('networkidle')
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                await page.context.add_cookies([cookie])
        await page.goto("https://twitter.com/home")
        url = page.url
    except FileNotFoundError:
        time.sleep(60)
        cookies = page.get_cookies()
        with open("cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                await page.context.add_cookies([cookie])
        await page.goto("https://twitter.com/home")
    if Post != None:
        await page.fill("//*[@data-testid=\"tweetTextarea_0\"]", Post)
        await page.click("//*[text()='Post']")
    if tweetUrl != None:
        await page.goto(tweetUrl)
        if retweet != None:
            await page.click("//*[@data-testid=\"retweet\"]")
            await page.click("//*[text()='Repost']")
        if like != None:
            await page.click("//*[@data-testid=\"like\"]")
        if comment != None:
            await page.fill("//*[@data-testid=\"tweetTextarea_0\"]",comment)
            await page.click("//*[text()='Reply']")
    #input("Press Enter to close the browser...")
    #await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

def execute():
    asyncio.run(main())

@app.route('/')
def refresh():
    x = Thread(target=execute)
    x.start()
    return "Refreshed successfully: "+url

@app.route('/post')
def post():
    global Post
    Post = request.args.get('msg')
    x = Thread(target=execute)
    x.start()
    return "Refreshed successfully: "+url


@app.route('/all')
def allActions():
    global retweet
    global like
    global comment
    global tweetUrl
    tweetUrl = request.args.get('url')
    retweet =request.args.get('r')
    like = request.args.get('l')
    comment = request.args.get('msg')
    x = Thread(target=execute)
    x.start()
    return "Refreshed successfully: "+url

#asyncio.run(main())


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9708)
