"""
Script to set up and initialize Google Sheets for the TechSolutions website.
This will create the necessary Google Sheets if they don't exist
and set up the required headers.
"""

import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import (
    GOOGLE_SHEETS_CREDENTIALS,
    CONTACT_SHEET_NAME,
    JOB_APPLICATIONS_SHEET_NAME,
    USER_ACCOUNTS_SHEET_NAME
)

def setup_sheets():
    """
    Set up the required Google Sheets for the application
    """
    print("Setting up Google Sheets for TechSolutions website...")
    
    # Check if credentials file exists
    if not os.path.exists(GOOGLE_SHEETS_CREDENTIALS):
        print(f"Error: Credentials file '{GOOGLE_SHEETS_CREDENTIALS}' not found.")
        print("Please download your service account credentials JSON file from the Google Cloud Console")
        print("and save it as credentials.json in the backend directory.")
        sys.exit(1)
    
    # Define the scope
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    try:
        # Authenticate with Google Sheets
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            GOOGLE_SHEETS_CREDENTIALS, scope)
        client = gspread.authorize(credentials)
        
        print("Successfully authenticated with Google Sheets API")
        
        # Get service account email for sharing instructions
        with open(GOOGLE_SHEETS_CREDENTIALS, 'r') as f:
            import json
            creds_data = json.load(f)
            service_account_email = creds_data.get('client_email')
        
        # Create and set up Contact Form sheet
        setup_contact_form_sheet(client)
        
        # Create and set up Job Applications sheet
        setup_job_applications_sheet(client)
        
        # Create and set up User Accounts sheet
        setup_user_accounts_sheet(client)
        
        print("\nAll sheets have been set up successfully!")
        print(f"\nIMPORTANT: Make sure to share all these sheets with the service account email:")
        print(f"{service_account_email}")
        print("Give it 'Editor' permissions to allow the application to write to the sheets.")
        
    except Exception as e:
        print(f"Error setting up Google Sheets: {e}")
        sys.exit(1)

def setup_contact_form_sheet(client):
    """Set up the Contact Form submissions sheet"""
    sheet_name = CONTACT_SHEET_NAME
    headers = [
        "First Name", 
        "Last Name", 
        "Email", 
        "Phone", 
        "Company", 
        "Subject", 
        "Message", 
        "Timestamp"
    ]
    
    try:
        # Try to open the sheet, create it if it doesn't exist
        try:
            sheet = client.open(sheet_name).sheet1
            print(f"Found existing sheet: {sheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            sheet = client.create(sheet_name).sheet1
            print(f"Created new sheet: {sheet_name}")
        
        # Check if headers are already set
        existing_headers = sheet.row_values(1)
        if not existing_headers:
            # Set headers
            sheet.append_row(headers)
            print(f"Added headers to {sheet_name}")
        else:
            print(f"Headers already exist in {sheet_name}")
            
    except Exception as e:
        print(f"Error setting up Contact Form sheet: {e}")
        raise

def setup_job_applications_sheet(client):
    """Set up the Job Applications sheet"""
    sheet_name = JOB_APPLICATIONS_SHEET_NAME
    headers = [
        "Job Position",
        "First Name", 
        "Last Name", 
        "Email", 
        "Phone", 
        "Resume URL", 
        "Cover Letter", 
        "Portfolio URL", 
        "Timestamp"
    ]
    
    try:
        # Try to open the sheet, create it if it doesn't exist
        try:
            sheet = client.open(sheet_name).sheet1
            print(f"Found existing sheet: {sheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            sheet = client.create(sheet_name).sheet1
            print(f"Created new sheet: {sheet_name}")
        
        # Check if headers are already set
        existing_headers = sheet.row_values(1)
        if not existing_headers:
            # Set headers
            sheet.append_row(headers)
            print(f"Added headers to {sheet_name}")
        else:
            print(f"Headers already exist in {sheet_name}")
            
    except Exception as e:
        print(f"Error setting up Job Applications sheet: {e}")
        raise

def setup_user_accounts_sheet(client):
    """Set up the User Accounts sheet"""
    sheet_name = USER_ACCOUNTS_SHEET_NAME
    headers = [
        "Email",
        "Password Hash",
        "Name",
        "Registration Date"
    ]
    
    try:
        # Try to open the sheet, create it if it doesn't exist
        try:
            sheet = client.open(sheet_name).sheet1
            print(f"Found existing sheet: {sheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            sheet = client.create(sheet_name).sheet1
            print(f"Created new sheet: {sheet_name}")
        
        # Check if headers are already set
        existing_headers = sheet.row_values(1)
        if not existing_headers:
            # Set headers
            sheet.append_row(headers)
            print(f"Added headers to {sheet_name}")
        else:
            print(f"Headers already exist in {sheet_name}")
            
    except Exception as e:
        print(f"Error setting up User Accounts sheet: {e}")
        raise

if __name__ == "__main__":
    setup_sheets()