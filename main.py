from auth import get_driver, login_to_linkedin
from scraper import scrape_profile
import json
import os

def save_data(profile_data):
    filename = profile_data["url"].split("/")[-2] + ".json"
    filepath = os.path.join("data", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved for {profile_data['url']}")

def main():
    print("Initializing browser...")
    driver = get_driver()

    print("Attempting login...")
    if not login_to_linkedin(driver):
        print("Login failed.")
        return

    urls = [
        "https://www.linkedin.com/in/lukaoniani/",
        "https://www.linkedin.com/in/ani-cheghelidze/"
    ]

    for url in urls:
        print(f"\nScraping profile: {url}")
        data = scrape_profile(driver, url)
        print(f"Scraped data: {data}")
        save_data(data)

    driver.quit()

if __name__ == "__main__":
    main()
