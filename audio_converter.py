from pydub import AudioSegment
import os
import traceback
from pathlib import Path

def convert_to_mp3(audio_file):
    """
    Convert the downloaded audio file to MP3 format.
    
    :param audio_file: Path to the input audio file
    :return: Path to the MP3 file if successful, None otherwise
    """
    try:
        name, _ = os.path.splitext(audio_file)
        mp3_file = f"{name}.mp3"
        
        audio = AudioSegment.from_wav(audio_file)
        audio.export(mp3_file, format="mp3")
        
        # Remove the original WAV file
        os.remove(audio_file)
        
        print(f"Successfully converted {audio_file} to {mp3_file}")
        return mp3_file
    except FileNotFoundError:
        print(f"Error: Input file {audio_file} not found")
    except AudioSegment.CouldntDecodeError:
        print(f"Error: Unable to decode {audio_file}. The file might be corrupted or in an unsupported format.")
    except Exception as e:
        print(f"Unexpected error converting {audio_file} to MP3:")
        print(traceback.format_exc())
    return None

def cleanup_files(*files):
    """
    Clean up temporary files.
    
    :param files: Variable number of file paths to clean up
    """
    for file in files:
        try:
            if file and os.path.exists(file):
                os.remove(file)
                print(f"Cleaned up file: {file}")
        except Exception as e:
            print(f"Error cleaning up {file}: {str(e)}")
