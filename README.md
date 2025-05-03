# TechSolutions - Dark Themed Bootstrap 5 Website with Gemini AI Chatbot

This project is a responsive, dark-themed website for a software development company, built with Bootstrap 5 and featuring a Gemini AI-powered chatbot. The website includes various pages such as Home, About, Services, Pricing, FAQ, Careers, and Contact forms integrated with Google Sheets for data storage.

## Features

- Responsive dark-themed design using Bootstrap 5
- Multiple pages with modern UI components
- Gemini AI-powered chatbot for user assistance
- Google Sheets integration for form submissions
- Login/Registration functionality
- Mobile-friendly layout

## Project Structure

```
project/
├── index.html (Home)
├── about.html
├── services.html
├── contact.html
├── faq.html
├── pricing.html
├── careers.html
├── login.html
├── register.html
├── css/
│   ├── style.css
│   └── chat.css
├── js/
│   ├── script.js
│   └── chat.js
├── backend/
│   ├── app.py
│   ├── gemini_chatbot.py
│   ├── google_sheets_integration.py
│   ├── requirements.txt
│   ├── .env.template
│   └── credentials.json (you need to create this)
├── uploads/ (created automatically)
└── README.md
```

## Setup Instructions

### Frontend Setup

The frontend is built with HTML, CSS, and JavaScript and can be served by any web server. No build process is required.

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/techsolutions-website.git
   cd techsolutions-website
   ```

2. Serve the frontend files using a web server of your choice. For development, you can use Python's built-in HTTP server:
   ```
   python -m http.server 8000
   ```
   
   Then access the website at `http://localhost:8000`

### Backend Setup

The backend requires Python 3.7+ and several dependencies.

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file by copying `.env.template`:
   ```
   cp .env.template .env
   ```

6. Edit the `.env` file and add your API keys and settings.

7. Set up Google Sheets API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Sheets API and Google Drive API
   - Create service account credentials
   - Download the credentials JSON file and save it as `credentials.json` in the backend directory
   - Create the necessary Google Sheets (see below)

8. Set up Google Gemini API:
   - Go to [Google AI Studio](https://ai.google.dev/)
   - Get an API key
   - Add the API key to your `.env` file

9. Start the backend server:
   ```
   python app.py
   ```
   
   The backend will run at `http://localhost:5000`

### Required Google Sheets

You need to create the following Google Sheets in your Google Drive and share them with the service account email:

1. **TechSolutions Contact Form Submissions** - For contact form data
   - Columns: First Name, Last Name, Email, Phone, Company, Subject, Message, Timestamp

2. **TechSolutions Job Applications** - For job application data
   - Columns: Job Position, First Name, Last Name, Email, Phone, Resume URL, Cover Letter, Portfolio URL, Timestamp

3. **TechSolutions User Accounts** - For user registration data
   - Columns: Email, Password Hash, Name, Registration Date

Share these sheets with the service account email from your `credentials.json` file with Editor permissions.

## Deployment

### Frontend Deployment

You can deploy the frontend to any static hosting service:

1. **GitHub Pages**:
   - Push the code to a GitHub repository
   - Enable GitHub Pages in the repository settings
   - Choose the main branch as the source

2. **Netlify**:
   - Connect your GitHub repository to Netlify
   - Configure the build settings (not needed for this project)
   - Deploy the site

### Backend Deployment

The backend can be deployed to various platforms:

1. **Heroku**:
   - Create a new Heroku app
   - Add the required environment variables in Heroku settings
   - Deploy the backend directory to Heroku

2. **Railway** or **Render**:
   - Connect your GitHub repository
   - Configure the environment variables
   - Deploy the backend

3. **VPS/Cloud Server** (AWS, GCP, Azure, DigitalOcean, etc.):
   - Provision a server
   - Install Python and dependencies
   - Set up environment variables
   - Use Gunicorn and Nginx for production deployment

## Configuration

### Adjusting the Backend URL

In both `js/script.js` and `js/chat.js`, update the `API_URL` constant to point to your deployed backend:

```javascript
const API_URL = 'https://your-backend-url.com/api';
```

### Customizing the Chatbot

To customize the chatbot's behavior, modify the `SYSTEM_PROMPT` in `backend/gemini_chatbot.py`.

## Maintenance

- Regularly update dependencies to ensure security and compatibility
- Monitor Google Sheets API usage to stay within free tier limits
- Keep your Gemini API key secure and monitor usage

## License

This project is licensed under the MIT License - see the LICENSE file for details.