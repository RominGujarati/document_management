# Document Management System

## Overview

This project is a Django-based Document Management System (DMS) that allows users to securely upload, view, and manage files of any type. The system is designed with scalability in mind to handle large files (hundreds of MB to GB) and includes user authentication and authorization features to ensure that users can only access their own files. Additionally, the system can be extended with a chatbot feature for querying documents.

## Features

### Core Features
- **File Upload**: Upload files of any type to the system. Files can be organized in folders.
- **File Viewing**: List all uploaded files and view their contents directly through the web interface.
- **File Deletion**: Delete files as needed from the system.
- **File Download**: Download files from storage to the server and further to a local directory.
- **Scalability**: Designed to handle large files, with provisions for efficient storage and retrieval.
- **Cloud Storage**: Files are stored on AWS S3. If S3 is not available, files are stored locally on disk.
- **User Authentication and Authorization**: Users must sign up and log in to access the system. Each user can only view and manage their own files.

### Chatbot
- **Document Querying**: Integrated a chatbot where users can ask questions about the documents they have uploaded.

### Setup Instructions

1. **Clone the Repository:**
   git clone https://github.com/RominGujarati/document_management.git
   cd document_management

2. **Install Dependencies:**
    pip install -r requirements.txt

3. **Database and AWS S3 Configuration:**
    Update the settings.py file with your database and aws s3 configurations or create .env using .env.example and add values there
    Run the following commands to set up the database:
        python manage.py makemigrations
        python manage.py migrate

4. **Run the Development Server & Access the Application:**
    python manage.py runserver
    Open a web browser and navigate to http://localhost:8000.
