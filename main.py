from flask import Flask
from app import app as application
from dotenv import load_dotenv
import os

# Load environment variables from .env file in development
if os.path.exists('.env'):
    load_dotenv()

# Vercel requires the app to be named 'app'
app = application

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
