from flask import Flask
from app import app as application
from dotenv import load_dotenv
import os
from lambda_setup import setup_ffmpeg

# Load environment variables from .env file in development
if os.path.exists('.env'):
    load_dotenv()

# Set up ffmpeg in Lambda environment
if os.environ.get('VERCEL') == '1':
    setup_ffmpeg()

# Vercel requires the app to be named 'app'
app = application

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
