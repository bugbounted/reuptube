import os
from playwright.sync_api import Playwright, sync_playwright
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Playwright download function
def download_video(video_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to video URL
        page.goto(video_url)

        # Wait for video to load
        page.wait_for_selector("#video-title")

        # Get the video source URL
        video_source = page.query_selector("#player video").get_attribute("src")

        # Download the video
        page.goto(video_source)

        # Wait for download to complete
        page.wait_for_download()

        # Rename downloaded file
        os.rename(os.path.join(os.path.expanduser("~"), "Downloads", "video.mp4"), "final.mp4")

        # Clean up
        browser.close()


# Selenium upload function
def upload_video(video_path):
    # Set up browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)

    # Log in to YouTube
    browser.get("https://www.youtube.com/upload")
    email_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(os.environ.get("GMAIL_USERNAME"))
    email_input.send_keys(Keys.RETURN)
    password_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(os.environ.get("GMAIL_PASSWORD"))
    password_input.send_keys(Keys.RETURN)

    # Wait for upload page to load
    browser.get("https://www.youtube.com/upload")
    browser.find_element_by_xpath("//span[contains(text(), 'Video')]//parent::button").click()
    browser.find_element_by_id("file-loader").send_keys(os.path.abspath(video_path))

    # Wait for upload to complete
    WebDriverWait(browser, 600).until(EC.url_contains("video_manager"))

    # Clean up
    browser.quit()


# Main function
def main():
    # Get YouTube index page
    index_page = "https://www.youtube.com"

    # Download video
    download_video(index_page)

    # Upload video
    upload_video("final.mp4")


if __name__ == "__main__":
    main()
