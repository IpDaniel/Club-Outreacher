from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


def process_search_terms(search_terms, driver, file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    club_access_details = []

    for search_term in search_terms:
        for _, row in df.iterrows():
            url = row['link']
            school = row['school']
            city = row['city']
            
            # Get clubs for the current search term and URL
            clubs = get_clubs(driver, url, search_term)
            
            # Create a dictionary for each club and append to the list
            for club_url in clubs:
                club_detail = {
                    'city': city,
                    'school': school,
                    'url': club_url
                }
                club_access_details.append(club_detail)
                print("added club with these details: " + str(club_detail))
    
    # Create a DataFrame from the list of dictionaries
    result_df = pd.DataFrame(club_access_details)
    
    # Save the DataFrame as an Excel file
    result_df.to_excel('club_access_details.xlsx', index=False)

    return club_access_details




# Function to get all the clubs that match the base url and search term
def get_clubs(driver, base_url, search_term):
    # Construct the full URL with the search term
    url = base_url + '?query=' + search_term

    try:
        # Navigate to the URL
        driver.get(url)
        time.sleep(5)
        
        # Get the page source after JavaScript has rendered the content
        page_source = driver.page_source

        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html5lib')

        # Find and return club links (adjust selectors as needed)
        club_list = soup.find('div', id='org-search-results')
        if club_list:
            club_a_list = club_list.find_all('a')
            club_link_list = []
            for club in club_a_list:
                print("found club with href: " + club.get('href') + ", and text: " + club.text.strip())
                club_link_list.append('https://' + base_url.split('/')[2] + club.get('href'))
            return club_link_list
        else:
            print(f"Club list not found for url {url} and search term {search_term}. Check the page structure.")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []



# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)
# chrome_options.add_argument("--disable-popup-blocking")  # Block popups


# Create a new Selenium WebDriver instance
driver = webdriver.Chrome(options=chrome_options)
search_terms = ['consulting', 'marketing']
process_search_terms(search_terms, driver, 'data/school-club-website-base-links.xlsx')
driver.quit()