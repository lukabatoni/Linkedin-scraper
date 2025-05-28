from selenium.webdriver.common.by import By
import time

def scrape_profile(driver, url):
    data = {
        'name': '',
        'headline': '',
        'about': '',
        'experience': [],
        'education': '',
        'company': '',
        'location': '',
        'connections': '',
        'url': url,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        print(f"\nAttempting to scrape: {url}")
        driver.get(url)
        time.sleep(5)

        # Name
        try:
            data['name'] = driver.find_element(By.XPATH, '//h1[contains(@class,"text-heading-xlarge")]').text
        except:
            print("Could not find name.")

        # Headline
        try:
            data['headline'] = driver.find_element(By.XPATH, '//div[@class="body-small text-color-text"]/span').text
        except:
            print("Could not find headline.")

        # Education
        try:
            data['education'] = driver.find_element(By.XPATH, '//div[contains(@class, "body-small text-color-text-low-emphasis")]/span[1]').text
        except:
            print("Could not find education.")

        # Company
        try:
            data['company'] = driver.find_element(By.XPATH, '//span[@class="member-current-company"]').text
        except:
            print("Could not find company.")

        # Location
        try:
            data['location'] = driver.find_element(By.XPATH, '//div[contains(@class, "body-small text-color-text-low-emphasis")][2]').text.split('\n')[0]
        except:
            print("Could not find location.")

        # Connections
        try:
            data['connections'] = driver.find_element(By.XPATH, '//span[contains(@class, "whitespace-nowrap")]').text
        except:
            print("Could not find connections.")

        # Experience
        try:
            experience_section = driver.find_element(By.XPATH, '//section[contains(@id,"experience")]')
            experience_items = experience_section.find_elements(By.XPATH, './/li[contains(@class,"artdeco-list__item")]')
            
            for item in experience_items:
                try:
                    title = item.find_element(By.XPATH, './/span[contains(@class, "mr1")]/span').text
                except:
                    title = ''
                try:
                    company = item.find_element(By.XPATH, './/span[contains(@class,"t-14 t-normal")]/span').text
                except:
                    company = ''
                try:
                    date_range = item.find_element(By.XPATH, './/span[contains(@class,"t-14 t-normal t-black--light")][1]/span').text
                except:
                    date_range = ''
                try:
                    location = item.find_element(By.XPATH, './/span[contains(@class,"t-14 t-normal t-black--light")][2]/span').text
                except:
                    location = ''

                data['experience'].append({
                    'title': title,
                    'company': company,
                    'date_range': date_range,
                    'location': location
                })
        except:
            print("Could not find experience section.")

        return data

    except Exception as e:
        print(f"Failed to scrape {url}: {str(e)}")
        return data
