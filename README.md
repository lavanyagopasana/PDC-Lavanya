# PDC-Lavanya


# Project Overview

This project is a Flask web application created for the PDC evaluation task. It demonstrates:

Google Authentication using OAuth 2.0

Displaying user profile info (name, email, profile picture)

Showing the current Indian time

Generating a diamond pattern with rotated text based on user input

A simple, clean, and responsive UI

# Features

# Phase 1: Authentication

Sign in with Google

Display user name, email, and profile picture (optional)

Show current Indian time

Sign out functionality

# Phase 2: Diamond Pattern

Input box for Number of Lines (maximum 100)

Displays a diamond pattern with rotated text

Pattern output is centered and uses a monospace font

Back button to return to the main page


# Setup Instructions

# Clone the repository

git clone https://github.com/lavanyagopasana/PDC-Lavanya1.git
cd PDC-Lavanya


# Create a virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


# Install dependencies

pip install -r requirements.txt

# Add Google OAuth credentials

Place your client_secret.json file in the project root (download from Google Cloud Console).

# Run the application

python app.py

# Open your browser at:

http://127.0.0.1:5000/

# Notes

Ensure Number of Lines ≤ 100 when generating the diamond pattern.

The output is centered and formatted using monospace font for correct alignment.

Sign-in button and UI are designed to be clean and professional.

# Author

Lavanya Gopasana

Email: lavanyagopasana@gmail.com

GitHub: github.com/lavanyagopasana
