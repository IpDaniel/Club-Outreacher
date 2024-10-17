# Automated Club Outreach System

This project is a collection of scripts designed to automate the process of sending customized cold outreach emails to university clubs based on specific focus areas and an outreach purpose prompt. The system streamlines the process of gathering club information, generating personalized email content, and sending emails at scale.

## Overview

The Automated Club Outreach System consists of several Python scripts that work together to:

1. Scrape lists of clubs and basic access information from university websites
2. Process and store club details
3. Generate customized outreach email content for each club using AI
4. Send personalized emails to club contacts

## Components

### 1. Club Information Collection (`findclubs.py`)

This script uses Selenium and BeautifulSoup to:
- Navigate through university club directory websites
- Search for clubs based on specified keywords (e.g., 'consulting', 'marketing')
- Extract basic club information and URLs

### 2. Club Detail Extraction (`collect_club_info.py`)

This script:
- Visits individual club pages
- Extracts detailed information such as club name, description, email, and phone number
- Stores the collected data in an Excel file

### 3. Email Content Generation (`write_emails.py`)

Using OpenAI's GPT model, this script:
- Reads club information from the Excel file
- Generates personalized email subject lines and content based on a provided prompt
- Assigns a compatibility score to each generated email
- Saves the results in a new Excel file

### 4. Email Sending (`send_emails.py`)

This final script:
- Reads the Excel file containing generated email content
- Filters clubs based on a compatibility threshold
- Sends emails using SMTP to clubs that meet the threshold

## Setup and Usage

1. Install required dependencies:
   ```
   pip install selenium beautifulsoup4 pandas openpyxl openai
   ```

2. Set up environment variables for email credentials and OpenAI API key.

3. Prepare input files:
   - `school-club-website-base-links.xlsx`: List of university club directory URLs
   - `prompt.txt`: Outreach purpose prompt for email generation
   - These should go in a 'data' folder stored at the project folder level

4. Run the scripts in order:
   ```
   python scripts/findclubs.py
   python scripts/collect_club_info.py
   python scripts/write_emails.py
   python scripts/send_emails.py
   ```

## Customization

- Modify search terms in `findclubs.py` to target specific types of clubs
- Adjust the compatibility threshold in `send_emails.py` to control email sending criteria
- Update the prompt in `prompt.txt` to change the focus of your outreach campaign

## Notes

- Ensure compliance with email regulations and university policies when using this system
- Monitor and respect rate limits for web scraping and API usage
- Regularly update the scripts to accommodate changes in website structures or API versions

