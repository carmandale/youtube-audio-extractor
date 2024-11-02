import os
import subprocess
import sys
import shutil
import stat
import logging

def setup_ffmpeg():
    """Set up ffmpeg in Lambda environment"""
    if os.environ.get('VERCEL') != '1':
        return True
        
    try:
        temp_dir = '/tmp'
        ffmpeg_dir = os.path.join(temp_dir, 'ffmpeg')
        ffmpeg_bin = os.path.join(ffmpeg_dir, 'ffmpeg')
        
        # If ffmpeg already exists and is executable, we're done
        if os.path.exists(ffmpeg_bin) and os.access(ffmpeg_bin, os.X_OK):
            logging.info("FFmpeg already installed and executable")
            return True
        
        # Create directory for ffmpeg
        os.makedirs(ffmpeg_dir, mode=0o777, exist_ok=True)
        
        # Download static ffmpeg binary directly
        logging.info("Downloading FFmpeg...")
        download_url = 'https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/ffmpeg-linux-x64'
        subprocess.run([
            'curl', '-L', download_url,
            '-o', ffmpeg_bin
        ], check=True)
        
        # Make executable
        os.chmod(ffmpeg_bin, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        # Verify installation
        if os.path.exists(ffmpeg_bin) and os.access(ffmpeg_bin, os.X_OK):
            logging.info(f"FFmpeg installed successfully at {ffmpeg_bin}")
            return True
        else:
            logging.error("FFmpeg installation failed - binary not found or not executable")
            return False
            
    except Exception as e:
        logging.error(f"Error setting up ffmpeg: {str(e)}")
        return False