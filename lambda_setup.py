import os
import subprocess
import sys
import shutil
import stat
import logging

def setup_ffmpeg():
    """Set up ffmpeg in Lambda environment"""
    # First check if ffmpeg is available in PATH
    if shutil.which('ffmpeg'):
        return True
        
    # Check if we're in Vercel environment
    if os.environ.get('VERCEL') == '1':
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
            
            # Download static ffmpeg build
            logging.info("Downloading FFmpeg...")
            download_url = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
            subprocess.run(['curl', '-L', download_url, '-o', '/tmp/ffmpeg.tar.xz'], check=True)
            
            # Extract FFmpeg
            logging.info("Extracting FFmpeg...")
            subprocess.run(['tar', 'xf', '/tmp/ffmpeg.tar.xz', '-C', ffmpeg_dir, '--strip-components=1'], check=True)
            
            # Make executable and set permissions
            os.chmod(ffmpeg_bin, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0o777
            
            # Verify installation
            if os.path.exists(ffmpeg_bin) and os.access(ffmpeg_bin, os.X_OK):
                logging.info(f"FFmpeg installed successfully at {ffmpeg_bin}")
                # Add to PATH
                os.environ['PATH'] = f"{ffmpeg_dir}:{os.environ.get('PATH', '')}"
                return True
            else:
                logging.error("FFmpeg installation failed - binary not found or not executable")
                return False
                
        except Exception as e:
            logging.error(f"Error setting up ffmpeg: {str(e)}")
            return False
    
    return False