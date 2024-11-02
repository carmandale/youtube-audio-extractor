import yt_dlp
import os
import traceback
import re
import tempfile
from pathlib import Path
import logging

def sanitize_filename(title):
    """Clean the title to make it filesystem-friendly"""
    # Remove invalid characters and trim spaces
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    clean_title = clean_title.strip()
    # Limit length to avoid too long filenames
    return clean_title[:100]

def download_audio(video_url, default_title="video"):
    """
    Download audio from a YouTube video.
    
    :param video_url: URL of the YouTube video
    :param default_title: Default title if none is found
    :return: Tuple of (file_path, video_title) or (None, None) if download fails
    """
    # Use temp directory directly
    temp_dir = tempfile.gettempdir()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    }

    # Add ffmpeg path if we're in Vercel environment
    if os.environ.get('VERCEL') == '1':
        ffmpeg_path = os.path.join(tempfile.gettempdir(), 'ffmpeg', 'ffmpeg')
        ydl_opts['ffmpeg_location'] = ffmpeg_path
        logging.info(f"Using ffmpeg from: {ffmpeg_path}")
        if not os.path.exists(ffmpeg_path):
            logging.error(f"FFmpeg not found at {ffmpeg_path}")
            return None, None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info("Starting download...")
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            video_title = info.get('title', default_title)
            base, _ = os.path.splitext(filename)
            wav_path = f"{base}.wav"
            logging.info(f"Download completed: {wav_path}")
            return wav_path, sanitize_filename(video_title)
    except Exception as e:
        logging.error(f"Error downloading audio: {str(e)}")
        logging.error(traceback.format_exc())
        return None, None
