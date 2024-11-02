import os
import subprocess
import sys

def setup_ffmpeg():
    """Set up ffmpeg in Lambda environment"""
    if not os.path.exists('/opt/ffmpeg/ffmpeg'):
        try:
            # Download and extract ffmpeg
            subprocess.run([
                'curl', '-L', 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz',
                '-o', '/tmp/ffmpeg.tar.xz'
            ])
            os.makedirs('/opt/ffmpeg', exist_ok=True)
            subprocess.run(['tar', 'xf', '/tmp/ffmpeg.tar.xz', '-C', '/opt/ffmpeg', '--strip-components=1'])
            os.chmod('/opt/ffmpeg/ffmpeg', 0o755)
        except Exception as e:
            print(f"Error setting up ffmpeg: {str(e)}")
            return False
    return True 