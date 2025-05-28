from auth import get_driver, login_to_linkedin
from scraper import scrape_profile, save_data
import time

def main():
    try:
        print("Initializing browser...")
        driver = get_driver()
        
        print("Attempting login...")
        if not login_to_linkedin(driver):
            print("Login failed. Check logs for details.")
            return
        
        # Test with your own profile first
        profiles = [
            'https://www.linkedin.com/in/lukaoniani/',  
            'https://www.linkedin.com/in/saba-beradzee/'
        ]
        
        for profile_url in profiles:
            print(f"\nStarting scrape for: {profile_url}")
            
            # Take screenshot before scraping for debugging
            driver.save_screenshot(f"debug_before_{profile_url.split('/')[-1]}.png")
            
            profile_data = scrape_profile(driver, profile_url)
            
            if profile_data:
                print("Scraped data:", profile_data)  # Debug output
                save_data(profile_data)
            else:
                print(f"Failed to scrape {profile_url}")
                
            # Take screenshot after scraping
            driver.save_screenshot(f"debug_after_{profile_url.split('/')[-1]}.png")
            
            print("Waiting before next request...")
            time.sleep(10)
        
        print("\nScraping complete!")
        
    except Exception as e:
        print(f"Fatal error in main: {str(e)}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()