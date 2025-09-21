from flask import Flask, redirect, request, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
from datetime import datetime
import pytz
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecret"  # Replace with a secure key

# --- DATABASE SETUP ---
import os

db_path = os.path.join(os.path.dirname(__file__), 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    picture = db.Column(db.String(300))
    last_login = db.Column(db.String(50))

# OAuth Setup
oauth = OAuth(app)
with open("client_secret.json") as f:
    secrets = json.load(f)["web"]

google = oauth.register(
    name='google',
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
        ist_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        return render_template_string("""
        <div style="
            max-width:500px;
            margin:50px auto;
            padding:30px;
            border-radius:12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            font-family: 'Segoe UI', sans-serif;
            text-align:center;
            background: #fdfdfd;
        ">
            {% if user.get('picture') %}
                <img src="{{user['picture']}}" alt="Profile Picture" style="border-radius:50%; width:120px; border:3px solid #4285F4;"><br><br>
            {% endif %}
            <h2 style="margin:10px 0; color:#333;">Hello {{user['name']}}</h2>
            <p style="color:#666; margin:5px 0;">Signed in as <strong>{{user['email']}}</strong></p>
            <p style="color:#444; margin:10px 0;">Current Indian Time: {{ist_time}}</p>
            <a href="{{url_for('logout')}}" style="
                display:inline-block;
                margin-top:15px;
                padding:10px 25px;
                border:none;
                border-radius:6px;
                background:#f44336;
                color:white;
                text-decoration:none;
                font-weight:bold;
                transition:0.3s;
            " onmouseover="this.style.background='#d32f2f'" onmouseout="this.style.background='#f44336'">Sign Out</a>

            <!-- Phase 2: Number of Lines Input -->
            <form method="POST" action="/design" style="margin-top:25px; display:flex; justify-content:center; gap:10px; align-items:center;">
                <input type="number" name="lines" max="100" placeholder="Number of Lines" required style="
                    padding:8px 12px;
                    border-radius:6px;
                    border:1px solid #ccc;
                    font-size:14px;
                    width:120px;
                    text-align:center;
                ">
                <button type="submit" style="
                    padding:8px 18px;
                    border:none;
                    border-radius:6px;
                    background:#4285F4;
                    color:white;
                    font-weight:bold;
                    font-size:14px;
                    cursor:pointer;
                    transition:0.3s;
                " onmouseover="this.style.background='#3367D6'" onmouseout="this.style.background='#4285F4'">
                    Display
                </button>
            </form>
        </div>

        """, user=user, ist_time=ist_time)

    # Creative Google sign-in button
    return render_template_string("""
    <div style="display:flex; justify-content:center; align-items:center; height:100vh; font-family: 'Segoe UI', sans-serif;">
        <a href="/login" style="text-decoration:none;">
            <button style="
                display:flex;
                align-items:center;
                gap:12px;
                background: #4285F4;  /* Clean Google blue */
                color:white;
                border:none;
                border-radius:8px;
                font-size:16px;
                font-weight:bold;
                padding:12px 25px;
                cursor:pointer;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.3)'" 
               onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 5px 15px rgba(0,0,0,0.2)'">
               <img src="{{ url_for('static', filename='img/g-logo.png') }}" alt="Google logo" style="width:22px; height:22px; background:white; border-radius:50%; padding:2px;">
                Sign in with Google
            </button>
        </a>
    </div>
    """)


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user_info = google.userinfo()  # Fetch full user info

    # Check if user already exists
    user = User.query.filter_by(google_id=user_info["sub"]).first()
    if not user:
        # New user → add to database
        user = User(
            google_id=user_info["sub"],
            name=user_info["name"],
            email=user_info["email"],
            picture=user_info.get("picture"),
            last_login=datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
    else:
        # Existing user → update last login
        user.last_login = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    
    db.session.commit()  # ✅ Very important to save changes
    session["user"] = {
        "name": user.name,
        "email": user.email,
        "picture": user.picture
    }
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/design", methods=["POST"])
def design():
    n = int(request.form['lines'])
    text = "FORMULAQSOLUTIONS"
    length = len(text)
    output = ""

    # Upper half of diamond (including middle)
    for i in range(n // 2 + 1):
        spaces = n // 2 - i
        output += " " * spaces

        newstr = ""
        # left side
        for j in range(i + 1):
            output += text[(i + j) % length]
            newstr += text[(i + j) % length]
        # right side
        for k in range(i, i * 2, 1):
            output += text[(i + k + 1) % length]
            newstr += text[(i + k + 1) % length]

        output += "\n"

    # Lower half of diamond
    for i in range(n // 2):
        spaces = i + 1
        output += " " * spaces
        # left half
        output += newstr[i + 1: len(newstr) - i - 1] + "\n"

    return f"""
    <div style='
        display:flex;
        justify-content:center;
        align-items:center;
        flex-direction:column;
        margin-top:50px;
        font-family: monospace;
        white-space: pre;
    '>
        <pre>{output}</pre>
        <a href='/' style='
            margin-top:20px;
            padding:8px 20px;
            background:#4285F4;
            color:white;
            border-radius:6px;
            text-decoration:none;
            font-weight:bold;
        '>Back</a>
    </div>
    """



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)
