from pydub import AudioSegment
import os
import traceback

def convert_to_mp3(audio_file):
    """
    Convert the downloaded audio file to MP3 format.
    
    :param audio_file: Path to the input audio file
    :return: True if conversion is successful, False otherwise
    """
    try:
        name, _ = os.path.splitext(audio_file)
        mp3_file = f"{name}.mp3"
        
        audio = AudioSegment.from_wav(audio_file)
        audio.export(mp3_file, format="mp3")
        
        # Remove the original WAV file
        os.remove(audio_file)
        
        print(f"Successfully converted {audio_file} to {mp3_file}")
        return True
    except FileNotFoundError:
        print(f"Error: Input file {audio_file} not found")
    except AudioSegment.CouldntDecodeError:
        print(f"Error: Unable to decode {audio_file}. The file might be corrupted or in an unsupported format.")
    except Exception as e:
        print(f"Unexpected error converting {audio_file} to MP3:")
        print(traceback.format_exc())
    return False
