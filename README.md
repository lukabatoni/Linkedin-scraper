LinkedinScraper
LinkedinScraper is a Python project for automating the extraction of public LinkedIn profile data using Selenium WebDriver.

Features
Automated login to LinkedIn
Scrapes key profile information:
Name
Headline
About
Experience
Education
Company
Location
Connections
Saves each profile’s data as a JSON file in the data directory
Requirements
Python 3.8 or higher
Google Chrome browser
ChromeDriver (managed automatically)
LinkedIn account credentials
Installation
Clone the repository:
git clone https://github.com/yourusername/LinkedinScraper.git
cd LinkedinScraper

pip install -r requirements.txt

Set up environment variables:

Create a file at .env with your LinkedIn credentials:
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
