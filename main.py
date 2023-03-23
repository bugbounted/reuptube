import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from playwright.sync_api import Playwright, sync_playwright_with_timeout
from youtube_dl import YoutubeDL

# Set up headless browser
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

# Set up playwright
with sync_playwright_with_timeout() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Set up YouTube credentials
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    # Log in to YouTube
    page.goto('https://accounts.google.com/signin')
    page.fill('input[type="email"]', email)
    page.click('div[jsname="V67aGc"]')
    page.wait_for_selector('input[type="password"]')
    page.fill('input[type="password"]', password)
    page.click('div[jsname="V67aGc"]')
    page.wait_for_selector('input[aria-label="Search"]')

    # Get the first video URL from the YouTube index page
    page.goto('https://www.youtube.com')
    video_link = page.query_selector('ytd-rich-item-renderer a[id="thumbnail"]')['href']

    # Download the video using youtube-dl
    ydl_opts = {
        'outtmpl': 'final.mp4'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

    # Upload the video to YouTube
    browser.get('https://www.youtube.com/upload')
    upload_input = browser.find_element_by_css_selector('input[type="file"]')
    upload_input.send_keys(os.path.abspath('final.mp4'))
    time.sleep(5)  # Wait for the upload to complete
    title_input = browser.find_element_by_css_selector('input[name="title"]')
    title_input.send_keys('My uploaded video')
    description_input = browser.find_element_by_css_selector('textarea[name="description"]')
    description_input.send_keys('This is my uploaded video')
    publish_button = browser.find_element_by_css_selector('button[data-action="publish"]')
    publish_button.click()

    # Close the browser
    browser.quit()