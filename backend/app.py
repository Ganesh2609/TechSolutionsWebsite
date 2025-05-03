import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import datetime
import threading
from dotenv import load_dotenv

# Import our custom modules
from google_sheets_integration import (
    setup_google_sheets, 
    submit_form_to_sheets, 
    verify_login_with_sheets,
    register_user_to_sheets
)
from gemini_chatbot import process_chat_message, reset_chat_session

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__, static_folder='../dist', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Configure file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def serve():
    """Serve the static frontend files"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    """Handle form submissions to Google Sheets"""
    try:
        # Process form data
        form_data = request.form.to_dict()
        form_type = form_data.get('formType', 'contact')
        
        # Add timestamp
        form_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle file uploads if present
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                # Generate a secure filename to prevent security issues
                filename = secure_filename(file.filename)
                unique_filename = f"{str(uuid.uuid4())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                # Add file URL to form data
                form_data['resumeUrl'] = f"/uploads/{unique_filename}"
        
        # Submit to Google Sheets
        result = submit_form_to_sheets(form_data, form_type)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        print(f"Error submitting form: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login verification"""
    try:
        data = request.json
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
            
        # Verify login credentials with Google Sheets
        result = verify_login_with_sheets(email, password)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 401
            
    except Exception as e:
        print(f"Error processing login: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        data = request.json
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not name or not email or not password:
            return jsonify({'success': False, 'error': 'All fields required'}), 400
            
        # Register user in Google Sheets
        result = register_user_to_sheets(name, email, password)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 409 if 'already registered' in result.get('error', '') else 500
            
    except Exception as e:
        print(f"Error processing registration: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages with Gemini AI"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('sessionId', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
            
        # Process the message with Gemini
        response = process_chat_message(user_message, session_id)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-chat', methods=['POST'])
def reset_chat():
    """Reset a chat session"""
    try:
        data = request.json
        session_id = data.get('sessionId', 'default')
        
        # Reset the chat session
        result = reset_chat_session(session_id)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error resetting chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Helper functions
def submit_form_to_sheets(form_data, form_type):
    """Submit form data to Google Sheets"""
    client = setup_google_sheets()
    if not client:
        return {'success': False, 'error': 'Unable to connect to Google Sheets'}
    
    try:
        if form_type == 'contact':
            sheet = client.open('TechSolutions Contact Form Submissions').sheet1
            # Prepare row data
            row = [
                form_data.get('firstName', ''),
                form_data.get('lastName', ''),
                form_data.get('email', ''),
                form_data.get('phone', ''),
                form_data.get('company', ''),
                form_data.get('subject', ''),
                form_data.get('message', ''),
                form_data.get('timestamp', '')
            ]
        elif form_type == 'application':
            sheet = client.open('TechSolutions Job Applications').sheet1
            # Prepare row data for job applications
            row = [
                form_data.get('jobPosition', ''),
                form_data.get('firstName', ''),
                form_data.get('lastName', ''),
                form_data.get('email', ''),
                form_data.get('phone', ''),
                form_data.get('resumeUrl', ''),
                form_data.get('coverLetter', ''),
                form_data.get('portfolioUrl', ''),
                form_data.get('timestamp', '')
            ]
        else:
            return {'success': False, 'error': 'Invalid form type'}
        
        # Append the row to the sheet
        sheet.append_row(row)
        
        return {'success': True, 'message': 'Form submitted successfully'}
        
    except Exception as e:
        print(f"Error submitting to sheets: {e}")
        return {'success': False, 'error': str(e)}

def verify_login_with_sheets(email, password):
    """Verify user login credentials against Google Sheets"""
    # Implementation moved to google_sheets_integration.py
    pass

def register_user_to_sheets(name, email, password):
    """Register a new user in Google Sheets"""
    # Implementation moved to google_sheets_integration.py
    pass

def process_chat_message(message, session_id):
    """Process a chat message with Gemini AI"""
    # Implementation moved to gemini_chatbot.py
    pass

def reset_chat_session(session_id):
    """Reset a chat session"""
    # Implementation moved to gemini_chatbot.py
    pass

if __name__ == '__main__':
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=5000)