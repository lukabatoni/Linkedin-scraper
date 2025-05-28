import json
import os
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_profile(driver, profile_url):
    try:
        print(f"\nAttempting to scrape: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)

        if 'authwall' in driver.current_url:
            print("Hit LinkedIn authwall - not properly logged in")
            return None

        data = {
            'name': '',
            'headline': '',
            'about': '',
            'experience': [],
            'education': [],
            'url': profile_url,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            name_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1'))
            )
            data['name'] = name_elem.text
        except Exception as e:
            print(f"Could not find name: {str(e)}")

        # Repeat similar for headline/about with correct XPATHs

        print(f"Successfully scraped data for {data['name']}")
        return data
    except Exception as e:
        print(f"Fatal error scraping profile: {str(e)}")
        return None

def save_data(data, filename='data/scraped_data.json'):
    """Save scraped data to JSON file"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save data in append mode
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')  # New line for each record
        logging.info(f"Successfully saved data for {data.get('name', 'unknown')}")
        print(f"Data saved for {data.get('name', 'unknown')}")  # Console confirmation
    except Exception as e:
        logging.error(f"Error saving data: {str(e)}")
        print(f"Error saving data: {str(e)}")  # Console error