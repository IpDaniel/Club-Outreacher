import os 
import csv
from openai import OpenAI
import pandas as pd



def create_script_for_row(row, query, ai_client):
    city = str(row['city'])
    school = str(row['school'])
    club_name = str(row['club_name'])
    club_description = str(row['club_description'])

    email_script = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": query + 
                "\ncity: " + city + 
                "\nschool: " + school + 
                "\nclub_name: " + club_name + 
                "\nclub_description: " + club_description
                }
            ]
        )
    return email_script.choices[0].message.content


def process_excel_and_create_emails(excel_file_path, query_file_path, ai_client, start_row=0, end_row=None):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Set the end row
    if (end_row is None):
        end_row = len(df)
    else:
        end_row = min(end_row, len(df))

    # Read the query from the text file
    with open(query_file_path, 'r') as file:
        query = file.read().strip()
    
    # Initialize an empty list to store the result dictionaries
    result_data = []
    
    # Iterate through each row in the DataFrame
    for _, row in df.iloc[start_row:end_row].iterrows():

        # Create email script for the current row
        email_script = create_script_for_row(row, query, ai_client)
        
        # Split the email script by '<<>>'
        script_parts = email_script.split('<<>>')
        
        # Create a new dictionary with email details and original row data
        result_dict = {
            'city': row['city'],
            'school': row['school'],
            'url': row['url'],
            'club_name': row['club_name'],
            'club_description': row['club_description'],
            'email': row['email'],
            'phone': row['phone'],
            'email_subject': script_parts[0].strip() if len(script_parts) > 0 else '',
            'email_content': script_parts[1].strip() if len(script_parts) > 1 else '',
            'compatibility_score': script_parts[2].strip() if len(script_parts) > 2 else ''
        }
        
        # Append the result dictionary to the list
        result_data.append(result_dict)
        print("Club processed: \n" + str(result_dict))
    
    # Create a DataFrame from the result_data list
    result_df = pd.DataFrame(result_data)
    
    # Save the DataFrame as an Excel file
    result_df.to_excel('data/clubs-with-scripts.xlsx', index=False)
    
    print(f"Excel file 'clubs-with-scripts.xlsx' has been created in the data folder.")

    return result_data

    
clubs_with_details = 'data/clubs-with-contact-info.xlsx'
query_file = 'data/prompt.txt'
client = OpenAI()

process_excel_and_create_emails(clubs_with_details, query_file, client)


