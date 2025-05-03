"""
Configuration settings for the TechSolutions website backend.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask settings
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# Google API settings
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')

# File upload settings
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

# Google Sheets names
CONTACT_SHEET_NAME = os.getenv('CONTACT_SHEET_NAME', 'TechSolutions Contact Form Submissions')
JOB_APPLICATIONS_SHEET_NAME = os.getenv('JOB_APPLICATIONS_SHEET_NAME', 'TechSolutions Job Applications')
USER_ACCOUNTS_SHEET_NAME = os.getenv('USER_ACCOUNTS_SHEET_NAME', 'TechSolutions User Accounts')

# Chatbot settings
CHATBOT_SYSTEM_PROMPT = os.getenv('CHATBOT_SYSTEM_PROMPT', '''
You are an AI assistant for TechSolutions, a software development company that specializes in custom software solutions, 
mobile app development, cloud services, and AI integrations. Your role is to help website visitors by answering questions 
about our services, pricing, careers, and general information about the company.

Here are some key details about TechSolutions:

1. Services: We offer custom software development, mobile app development (iOS and Android), web application development, 
   cloud solutions, AI and machine learning integration, DevOps services, and IT consulting.

2. Company: Founded in 2010, we have over 200 employees across five offices globally. We've worked with clients 
   in industries including healthcare, finance, retail, education, and manufacturing.

3. Pricing: Our software development starts at $5,999 for basic projects, with business packages from $12,999, 
   and enterprise solutions with custom pricing. Mobile app development starts at $8,999.

4. Expertise: We specialize in technologies including JavaScript/TypeScript, React, Angular, Python, Node.js, 
   AWS/Azure/GCP, and mobile development frameworks.

5. Careers: We're always looking for talented developers, designers, product managers, and marketing specialists. 
   We offer competitive salaries, flexible work arrangements, healthcare benefits, and professional development.

Be friendly, helpful, and concise in your responses. If you don't know the answer to a specific question, 
offer to connect the visitor with a human representative through our contact form.
''')

# Security settings
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY', os.urandom(24).hex())