import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import platform
import logging
import time
from selenium.webdriver.common.by import By

# Setup
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('config', exist_ok=True)
os.makedirs('chrome_profile', exist_ok=True)

logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_driver():
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={os.path.abspath('./chrome_profile')}")
    options.add_argument("--remote-debugging-port=9222")
    # options.add_argument("--headless")  # Optional for debugging
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2
    }
    options.add_experimental_option("prefs", prefs)

    chromedriver_path = os.path.join("drivers", "chromedriver.exe" if platform.system() == "Windows" else "chromedriver")
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def login_to_linkedin(driver):
    load_dotenv('config/.env')
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    try:
        driver.get('https://www.linkedin.com/login')
        time.sleep(3)

        if 'feed' in driver.current_url:
            logging.info("Already logged in via cookies")
            return True

        driver.find_element(By.ID, 'username').send_keys(email)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)

        if 'checkpoint' in driver.current_url:
            logging.warning("2FA required. Complete manually.")
            input("Complete 2FA and press Enter...")

        return True
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return False
