from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


def find_club_details(driver, link):
    driver.get(link)
    time.sleep(3)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html5lib')

    contact_info = {
        'club_name': None,
        'club_description': None,
        'email': None,
        'phone': None
    }

    # Find and set the club name
    try:
        title_heading = soup.find('h1', style='padding: 13px 0px 0px 85px;')
        title = title_heading.get_text()
        contact_info['club_name'] = title
        print(f'found title for {contact_info.get('club_name')}: {title}')
    except:
        contact_info['club_name'] = 'unknown'
        print(f'could not find title for {contact_info.get('club_name')}: {title}')

    # Find and set the club description 
    try:
        description_div = soup.find('div', class_=['bodyText-large', 'userSupplied'])
        description = description_div.get_text()
        contact_info['club_description'] = description
        print(f'found description for {contact_info.get('club_name')}: {description}')
    except:
        contact_info['club_description'] = 'unknown'
        print(f'could not find description for {contact_info.get('club_name')}: {description}')

    # Find and set the email address
    try:
        email_span = soup.find('span', string='Contact Email')
        parent_div = email_span.find_parent('div')
        email = parent_div.get_text(strip=True).split('EmailE:')[-1]
        contact_info['email'] = email
        print(f'found email for {contact_info.get('club_name')}: {email}')
    except:
        contact_info['email'] = 'unknown'
        print(f'could not find email for {contact_info.get('club_name')}')

    # Find and set the phone number
    try:
        phone_span = soup.find('span', string='Phone Number')
        parent_div = phone_span.find_parent('div')
        phone = parent_div.get_text(strip=True).split('Phone NumberP:')[-1]
        contact_info['phone'] = phone
        print(f'found phone number for {contact_info.get('club_name')}: {phone}')
    except:
        contact_info['phone'] = 'unknown'
        print(f'could not find phone number for {contact_info.get('club_name')}')
    
    # Return the contact info that was found
    return contact_info


def process_excel_and_find_details(driver, excel_file_path):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Initialize an empty list to store the combined dictionaries
    combined_data = []

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        link = row['url']
        
        # Get club details using the find_club_details function
        club_details = find_club_details(driver, link)
        
        # Combine the club details with the original row data
        combined_dict = {
            'url': row['url'],
            'city': row['city'],
            'school': row['school'],
            **club_details  # Unpack the club_details dictionary
        }
        
        # Append the combined dictionary to the list
        combined_data.append(combined_dict)
        print(f'processed page for {combined_dict['club_name']}')

    # Create a new DataFrame from the list of combined dictionaries
    result_df = pd.DataFrame(combined_data)

    # Save the resulting DataFrame as an Excel file
    result_df.to_excel('data/clubs-with-contact-info.xlsx', index=False)




# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)
# chrome_options.add_argument("--disable-popup-blocking")  # Block popups

# Create a new Selenium WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

process_excel_and_find_details(driver, 'data/club_access_details.xlsx')

