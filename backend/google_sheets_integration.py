import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup Google Sheets API connection
def setup_google_sheets():
    """
    Set up and return Google Sheets client
    """
    # Define the scope
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Load credentials from the service account file
    try:
        # Path to service account credentials JSON file
        # You need to create this file in the Google Cloud Console
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', scope)
        
        # Authorize the client
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Error setting up Google Sheets: {e}")
        return None

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    """
    Handle form submissions to Google Sheets
    """
    try:
        # Get data from the request
        data = request.json
        form_type = data.get('formType', 'contact')  # Default to contact form
        
        # Setup Google Sheets client
        client = setup_google_sheets()
        if not client:
            return jsonify({'success': False, 'error': 'Unable to connect to Google Sheets'}), 500
        
        # Open appropriate spreadsheet based on form type
        if form_type == 'contact':
            sheet = client.open('TechSolutions Contact Form Submissions').sheet1
            # Prepare row data
            row = [
                data.get('firstName', ''),
                data.get('lastName', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('company', ''),
                data.get('subject', ''),
                data.get('message', ''),
                data.get('timestamp', '')
            ]
        elif form_type == 'application':
            sheet = client.open('TechSolutions Job Applications').sheet1
            # Prepare row data for job applications
            row = [
                data.get('jobPosition', ''),
                data.get('firstName', ''),
                data.get('lastName', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('resumeUrl', ''),  # URL to the uploaded resume
                data.get('coverLetter', ''),
                data.get('portfolioUrl', ''),
                data.get('timestamp', '')
            ]
        elif form_type == 'login':
            sheet = client.open('TechSolutions User Accounts').sheet1
            # Prepare row data for user accounts
            row = [
                data.get('email', ''),
                data.get('passwordHash', ''),  # Store hashed password, not plain text
                data.get('registered', '')  # Timestamp of registration
            ]
        else:
            return jsonify({'success': False, 'error': 'Invalid form type'}), 400
        
        # Append the row to the sheet
        sheet.append_row(row)
        
        return jsonify({'success': True, 'message': 'Form submitted successfully'})
    
    except Exception as e:
        print(f"Error submitting form: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify-login', methods=['POST'])
def verify_login():
    """
    Verify user login credentials against Google Sheets
    """
    try:
        # Get login data from request
        data = request.json
        email = data.get('email', '')
        password = data.get('password', '')  # This would be hashed client-side
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Setup Google Sheets client
        client = setup_google_sheets()
        if not client:
            return jsonify({'success': False, 'error': 'Unable to connect to Google Sheets'}), 500
        
        # Open the users spreadsheet
        sheet = client.open('TechSolutions User Accounts').sheet1
        
        # Find the user by email
        try:
            cell = sheet.find(email)
            row = sheet.row_values(cell.row)
            
            # In a real application, you would properly verify the password hash
            # For demo purposes, we'll just check if it matches
            # WARNING: This is NOT secure for production!
            stored_password = row[1]
            
            if password == stored_password:  # In real app: check_password_hash(stored_password, password)
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
                
        except gspread.exceptions.CellNotFound:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"Error verifying login: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register_user():
    """
    Register a new user in Google Sheets
    """
    try:
        # Get registration data
        data = request.json
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')  # This would be hashed
        
        if not name or not email or not password:
            return jsonify({'success': False, 'error': 'All fields required'}), 400
        
        # Setup Google Sheets client
        client = setup_google_sheets()
        if not client:
            return jsonify({'success': False, 'error': 'Unable to connect to Google Sheets'}), 500
        
        # Open the users spreadsheet
        sheet = client.open('TechSolutions User Accounts').sheet1
        
        # Check if user already exists
        try:
            cell = sheet.find(email)
            return jsonify({'success': False, 'error': 'Email already registered'}), 409
        except gspread.exceptions.CellNotFound:
            # User doesn't exist, proceed with registration
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # In a real app, hash the password: password_hash = generate_password_hash(password)
            password_hash = password  # For demo only
            
            # Append new user
            sheet.append_row([email, password_hash, name, timestamp])
            
            return jsonify({'success': True, 'message': 'Registration successful'})
            
    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)