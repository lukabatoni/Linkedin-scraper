import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
import logging
import platform

# Create directories if they don't exist
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('config', exist_ok=True)
os.makedirs('chrome_profile', exist_ok=True)

# Set up logging
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

    # Your existing preferences
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2
    }
    options.add_experimental_option("prefs", prefs)

    # Your existing arguments
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # For LinkedIn, you might want to start without headless to handle login
    # options.add_argument("--headless")  # Comment this out initially
    
    # Add these for LinkedIn specifically
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={os.path.abspath('./chrome_profile')}")

    # Use your existing chromedriver.exe path
    chromedriver_path = os.path.join("drivers", "chromedriver.exe" if platform.system() == "Windows" else "chromedriver")
    service = Service(executable_path=chromedriver_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver
    except Exception as e:
        logging.error(f"Driver creation failed: {str(e)}")
        raise

def login_to_linkedin(driver):
    """Handle LinkedIn login with your existing driver"""
    load_dotenv('config/.env')
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    try:
        driver.get('https://www.linkedin.com/login')
        time.sleep(3)
        
        # Check if already logged in
        if 'feed' in driver.current_url:
            logging.info("Already logged in via cookies")
            return True
        
        # Fill in login form
        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        
        email_field.send_keys(email)
        password_field.send_keys(password)
        
        # Submit form
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)
        
        # Handle 2FA if needed
        if 'checkpoint' in driver.current_url:
            logging.warning("2FA required - please complete manually")
            input("Press Enter after completing 2FA...")
            time.sleep(3)
        
        return True
    
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return False