import os
import subprocess
import sys
import shutil

def setup_ffmpeg():
    """Set up ffmpeg in Lambda environment"""
    # First check if ffmpeg is available in PATH
    if shutil.which('ffmpeg'):
        return True
        
    # Check if we're in Vercel environment
    if os.environ.get('VERCEL') == '1':
        try:
            # Create directory for ffmpeg
            os.makedirs('/tmp/ffmpeg', exist_ok=True)
            
            # Download static ffmpeg build
            subprocess.run([
                'curl', '-L', 
                'https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/ffmpeg-linux-x64',
                '-o', '/tmp/ffmpeg/ffmpeg'
            ], check=True)
            
            # Make executable
            os.chmod('/tmp/ffmpeg/ffmpeg', 0o755)
            
            # Add to PATH
            os.environ['PATH'] = f"/tmp/ffmpeg:{os.environ.get('PATH', '')}"
            
            print("FFmpeg setup completed successfully")
            return True
        except Exception as e:
            print(f"Error setting up ffmpeg: {str(e)}")
            return False
    
    return False