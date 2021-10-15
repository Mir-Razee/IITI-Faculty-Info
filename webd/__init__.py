from flask import Flask
import sys
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

# Session config
app.secret_key = 'super-secret-key'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['RECAPTCHA_SITE_KEY'] = '6LdcB9IcAAAAAOiPYSOCtboOnItc5uylKFG-Kr5u' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '6LdcB9IcAAAAAE9Z22KQInYYIsK5sDWdmuDoPx3P' # <-- Add your secret key

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_PASSWORD"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
engine = create_engine(DATABASE_PASSWORD)##

#Check connection
try:
    conn = engine.connect()
except Exception as e:
    print('Connection Failed\nError Details:', e)
    sys.exit(1)
conn.close()

db = scoped_session(sessionmaker(bind=engine))


from webd import routes


