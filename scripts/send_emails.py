import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import pandas as pd

def process_and_send_emails(filepath, compatibility_threshold, sender_info):
    # Read the Excel file
    df = pd.read_excel(filepath)
    
    email_list = []
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Check if the compatibility score meets the threshold
        if float(row['compatibility_score']) >= compatibility_threshold:
            email_data = {
                'recipient_email': row['email'],
                'subject': row['email_subject'],
                'body': row['email_content']
            }
            email_list.append(email_data)
    
    # Call the send_emails function with the accumulated email list
    send_emails(sender_info['email'], sender_info['password'], email_list)



def send_emails(sender_email, sender_password, email_list):
    try:
        # Create SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Enable security
            # Login with sender credentials
            server.login(sender_email, sender_password)
            
            for email_data in email_list:
                # Create a multipart message
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = email_data['recipient_email']
                message["Subject"] = email_data['subject']

                # Add body to email
                message.attach(MIMEText(email_data['body'], "plain"))

                # Send email
                server.send_message(message)
                print(f"Email sent successfully to {email_data['recipient_email']}")

    except Exception as e:
        print(f"Error sending emails: {e}")


# I may want to remove the email address as an environment variable in the future
sender_info = {'email': os.environ.get('SEND_FROM_EMAIL_ADDRESS'), 
               'password': os.environ.get('SEND_FROM_EMAIL_PASSWORD')}

print(sender_info)

# process_and_send_emails('data/clubs-with-scripts.xlsx', 7, sender_info)
