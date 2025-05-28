import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_driver():
    """Initialize and return a Chrome WebDriver with persistent cookies"""
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./chrome_profile")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def login_to_linkedin(driver):
    """Handle LinkedIn login"""
    load_dotenv('config/.env')
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    
    if 'feed' in driver.current_url:
        logging.info("Already logged in via cookies")
        return True
    
    try:
        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        
        email_field.send_keys(email)
        password_field.send_keys(password)
        
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)
        
        if 'checkpoint' in driver.current_url:
            logging.warning("2FA required - please complete manually")
            input("Press Enter after completing 2FA...")
        
        return True
    
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return False