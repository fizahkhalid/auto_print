import os
import time
import logging
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from config import CHARTS, TIMEFRAMES_TO_SELENIUM_KEY  # Import chart URLs and timeframes from config


# Set up logging
logging.basicConfig(
    filename='chart_screenshot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize WebDriver with options
def init_driver(headless=True, width=1920, height=1080):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f"--window-size={width},{height}")
    driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    logging.info("WebDriver initialized successfully.")
    return driver

def load_url(driver, url):
    logging.info(f"Loading URL: {url}")
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    logging.info(f"URL loaded successfully: {url}")
    return driver

def load_timeframe(driver, timeframe_key):
    logging.info(f"Setting timeframe: {timeframe_key}")
    body_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    body_element.send_keys(timeframe_key + Keys.ENTER)
    time.sleep(3)  # Allowing time for the timeframe to load
    logging.info(f"Timeframe set to {timeframe_key}")
    return driver

def click_watchlist_icon(driver):
    logging.info("Clicking on the watchlist icon.")
    # element = driver.find_element(By.CSS_SELECTOR,
    #                               "body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--right > div > div.widgetbar-tabs > div > div > div > div > button:nth-child(1)")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, "body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--right > div > div.widgetbar-tabs > div > div > div > div > button:nth-child(1)"
    )))
    actions = ActionChains(driver)
    actions.click(element).perform()
    logging.info("Watchlist icon clicked.")
    time.sleep(1)
    return driver

# Function to take a screenshot for a specific chart and timeframe
def take_screenshot(chart, timeframe, save_path="screenshot.png"):
    url = CHARTS[chart]
    timeframe_key = TIMEFRAMES_TO_SELENIUM_KEY[timeframe]
    driver = init_driver()  # Initialize driver
    try:
        driver = load_url(driver, url)
        driver = load_timeframe(driver, timeframe_key)
        driver = click_watchlist_icon(driver)
        save_path = get_screenshot_path(chart, timeframe)
        driver.save_screenshot(save_path)
    finally:
        driver.quit()  # Ensure driver quits after the operation
    return save_path

# New function to take screenshots for all charts in CHARTS with the specified timeframe
def take_screenshots(timeframe):
    """
    Capture screenshots for all charts listed in CHARTS using a single WebDriver instance.
    This function reuses the same driver for efficiency, loading each URL and setting the timeframe in sequence.
    """
    timeframe_key = TIMEFRAMES_TO_SELENIUM_KEY[timeframe]
    driver = init_driver()  # Single driver instance for all charts
    screenshot_paths = {}
    try:
        WATCHLIST_CLOSED = False
        for chart, url in CHARTS.items():
            driver = load_url(driver, url)  # Load each chart URL
            driver = load_timeframe(driver, timeframe_key)  # Set timeframe for each chart
            
            if not WATCHLIST_CLOSED:
                driver = click_watchlist_icon(driver)
                WATCHLIST_CLOSED = True
              # Open necessary UI elements
            save_path = get_screenshot_path(chart, timeframe)  # Get unique save path
            driver.save_screenshot(save_path)  # Save screenshot
            screenshot_paths[chart] = save_path  # Store path in dictionary
       
    finally:
        driver.quit()  # Close driver after all screenshots are taken
    return screenshot_paths

# Function to get the file path for screenshots with timestamp
def get_screenshot_path(chart, timeframe):
    timestamp = datetime.now().strftime("%d_%m_%Y")  # Format changed to dd_mm_yyyy
    folder_directory = "charts"
    os.makedirs(folder_directory, exist_ok=True)
    return os.path.join(folder_directory, f"{chart}_{timeframe}_{timestamp}.png")
