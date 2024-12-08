# CloudNotes
## Description

CloudNotes is a small-scale web application built with Flask, a lightweight Python web framework. The project features user registration and login, the ability to upload and delete files, and integrates user-specific data storage. The application is designed for educational purposes, focusing on web development concepts like database management, session handling, and data privacy.


## Features
- User registration and login
- Upload and delete files
- User data deletion in accordance with GDPR
- Session management using Flask cookies
- SQLite database for storage
- Encryption of cookie and session data for security

## Technologies Used
- Flask – Web framework for building the application
- SQLite – Lightweight database used for storing user and file information
- PythonAnywhere – Hosting platform (for deployment)
- validator_collection – Used for email validation
- Python-dotenv – Used for managing environment variables (e.g., secret keys)

## Installation and Setup
### Requirements
- Python 3.x
- Flask
- SQLite (automatically included with Python)
- PythonAnywhere (for deployment, optional)

### Clone the repository
```bash
git clone https://github.com/janiejestemja/cloud_notes.git
cd cloud_notes
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Set up environment variables
Create a `.env` file in the project root and add the following line to set a secret key for Flask:
```makefile
SECRET_KEY=your_secret_key
```
You can generate a secure key using the `secrets` module in Python.
### Running the Application Locally
To run the application locally, use the following command:
```bash
flask run
```
*Your app will be available at http://127.0.0.1:5000/ by default.*

## Usage
- User Sign Up: Users can sign up with an email and password. Email addresses are validated using the validator_collection library.
- File Upload/Deletion: Users can upload and delete files, which are stored securely in the server’s file system.
- Account Deletion: Users can request account deletion, which will remove all their data from the system.

## Privacy and Data Protection
In compliance with the General Data Protection Regulation (GDPR), the application provides the following:
- Users can request their data at any time.
- Users can delete their account, along with all their uploaded data.
- All sensitive data is encrypted using Flask’s secret key.

## Deployment
For deployment, this project is hosted on PythonAnywhere. Once deployed, you can access your application at the provided URL. Please note that you may need to set up environment variables on the platform (for example, SECRET_KEY).

### Steps to Deploy on PythonAnywhere:
- Create an account on PythonAnywhere.
- Upload your project files.
- Set up a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
- Set the environment variable SECRET_KEY in the PythonAnywhere dashboard.
- Configure the web app settings on PythonAnywhere to point to the Flask application.

## License
This project is licensed under the MIT License – see the LICENSE file for details.
