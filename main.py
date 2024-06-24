import asyncio
import pickle
import time
from flask import Flask
from playwright.async_api import async_playwright

app = Flask(__name__)
url = ""


def load_cookies_from_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        cookies = pickle.load(f)
    return cookies


async def run(playwright):
    global url
    browser = await playwright.chromium.launch(headless=True, args = [
        '--disable-gpu',  # Disable GPU to save resources
        '--no-sandbox',  # No sandbox mode for faster launch
        '--disable-dev-shm-usage'  # Overcome limited resource problems
    ])
    context = await browser.new_context()
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
    #await page.fill("//*[@data-testid=\"tweetTextarea_0\"]",'hello')
    #input("Press Enter to close the browser...")
    #await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())


@app.route('/run')
def start():
    
    return "Refreshed successfully: "+url

@app.route('/')
def refresh():
    return "Refreshed successfully: "


#asyncio.run(main())


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9708)
