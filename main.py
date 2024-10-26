import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from config import charts,timeframes
try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    # driver = webdriver.Chrome()
except:
    pass
from selenium.webdriver.common.action_chains import ActionChains
    # print ("AF: No Chrome webdriver installed")
    # driver = webdriver.Chrome(ChromeDriverManager().install())

# Function to initialize WebDriver
def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=3840x2160")
    else:
        chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_url(driver,url):
    driver.get(url)
    time.sleep(3)
    return driver

def load_timeframe(driver,timeframe_key):
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_element.send_keys(timeframe_key+Keys.ENTER)
    time.sleep(3)
    return driver


def click_watchlist_icon(driver):
    element = driver.find_element(By.CSS_SELECTOR,"body > div.js-rootresizer__contents.layout-with-border-radius > div.layout__area--right > div > div.widgetbar-tabs > div > div > div > div > button:nth-child(1)")
    # Create an ActionChains object
    actions = ActionChains(driver)
    # Perform right-click on the element
    actions.click(element).perform()
    return driver

# Function to take screenshot
def take_screenshot(chart, timeframe,save_path="screenshot.png"):
    url = charts[chart]
    timeframe_key = timeframes[timeframe]
    driver = init_driver()
    driver = load_url(driver,url)
    driver = load_timeframe(driver,timeframe_key)
    driver = click_watchlist_icon(driver)
    save_path = get_screenshot_path(chart,timeframe)
    driver.save_screenshot(save_path)
    driver.quit()
    return save_path

# Function template for specific chart and timeframe
def get_screenshot_path(chart, timeframe):
    image_path = f"{chart}_{timeframe}.png"
    folder_directory = "charts"
    os.makedirs(folder_directory,exist_ok=True)
    save_path = os.path.join(folder_directory,image_path)
    return save_path
