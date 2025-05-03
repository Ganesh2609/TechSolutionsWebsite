# TechSolutions Website

A modern, responsive website for TechSolutions - a fictional tech company offering various IT services and solutions. This project includes both a frontend interface built with HTML, CSS, and JavaScript, and a backend API built with Flask.

![TechSolutions Website Screenshot](images/techsolutions-screenshot.png)

## Features

- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices
- **Modern UI**: Clean and professional interface with animations and interactive elements
- **Services Showcase**: Detailed information about the company's IT services
- **Team Section**: Highlights the team members with their expertise
- **Contact Form**: Integrated form that sends inquiries to the backend
- **Backend API**: Flask-based API for handling form submissions and data requests

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.7+ installed on your system
- Basic knowledge of HTML, CSS, and JavaScript
- A modern web browser (Chrome, Firefox, Safari, or Edge)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Ganesh2609/TechSolutionsWebsite.git
cd TechSolutionsWebsite
```

2. **Set up a virtual environment**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required dependencies**

```bash
pip install -r 'backend/requirements.txt'
```

If no requirements.txt file is available, install the following packages:

```bash
pip install flask flask-cors
```

### Running the Application

1. **Start the backend server**

```bash
python app.py
```

The Flask server should start running on `http://localhost:5000`.

2. **Open the website**

Simply open the `index.html` file in your web browser:

- Double-click the file in your file explorer, or
- Open it using your preferred web browser's "Open File" option, or
- Using a command like:
  ```bash
  # On Windows
  start index.html
  
  # On macOS
  open index.html
  
  # On Linux
  xdg-open index.html
  ```

3. **Explore the website**

Navigate through the different sections of the website to explore the services, team members, and other features.

## Technology Stack

- **Frontend**:
  - HTML5
  - CSS3 (with Flexbox/Grid for layouts)
  - JavaScript (ES6+)
  - Font Awesome (for icons)
  
- **Backend**:
  - Python
  - Flask