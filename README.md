# PDC-Lavanya

## Project Overview

This project is a **Flask web application** created for the **PDC evaluation task**. It demonstrates:

- **Google Authentication** using OAuth 2.0  
- **Displaying user profile info** (name, email, profile picture)  
- **Showing the current Indian time**  
- **Generating a diamond pattern** with rotated text based on user input  
- **A simple, clean, and responsive UI**

---

## Features

### Phase 1: Authentication

- **Sign in with Google**  
- **Display user name, email, and profile picture** (optional)  
- **Show current Indian time**  
- **Sign out functionality**

### Phase 2: Diamond Pattern

- **Input box for Number of Lines** (maximum 100)  
- **Displays a diamond pattern with rotated text**  
- **Pattern output is centered and uses a monospace font**  
- **Back button to return to the main page**

---

## Setup Instructions

# 1.Clone the repository

```bash
git clone https://github.com/lavanyagopasana/PDC-Lavanya1.git
cd PDC-Lavanya1

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add Google OAuth credentials
# This will create client_secret.json in the project root
cat > client_secret.json <<EOL
{
  "web": {
    "client_id": "<YOUR_CLIENT_ID>",
    "project_id": "<YOUR_PROJECT_ID>",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "<YOUR_CLIENT_SECRET>",
    "redirect_uris": [
      "http://127.0.0.1:5000/callback"
    ],
    "javascript_origins": [
      "http://127.0.0.1:5000"
    ]
  }
}
EOL

echo "client_secret.json created. Make sure to replace <YOUR_CLIENT_ID> and <YOUR_CLIENT_SECRET> with actual values."

# 5. Run the Flask application
python app.py

# 6. Open browser at
# http://127.0.0.1:5000/
