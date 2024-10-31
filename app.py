from flask import Flask, render_template, request, jsonify, send_file, session
from youtube_search import search_youtube
from audio_downloader import download_audio
from audio_converter import convert_to_mp3
from utils import create_summary_report
import threading
import logging
import os
import zipfile
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    session['processed_files'] = []  # Clear the list of processed files for each new session
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_videos():
    session['processed_files'] = []  # Clear the list of processed files for each new search
    primary_query = request.form['primary_query']
    secondary_query = request.form['secondary_query']
    limit = int(request.form['limit'])
    upload_date = request.form['upload_date']
    duration = request.form['duration']

    total_videos, videos = search_youtube(primary_query, secondary_query, limit, upload_date, duration)

    if not videos:
        return jsonify({
            "message": "No videos found matching the specified criteria.",
            "total_videos": total_videos,
            "videos": []
        })

    return jsonify({
        "message": "Search completed.",
        "total_videos": total_videos,
        "videos": videos
    })

@app.route('/process', methods=['POST'])
def process_videos():
    primary_query = request.form['primary_query']
    secondary_query = request.form['secondary_query']
    limit = int(request.form['limit'])
    upload_date = request.form['upload_date']
    duration = request.form['duration']

    def process_in_background():
        total_videos, videos = search_youtube(primary_query, secondary_query, limit, upload_date, duration)
        videos_to_process = len(videos)
        successful_downloads = 0
        successful_conversions = 0

        for video in videos:
            audio_file = download_audio(video['link'], video['title'])
            if audio_file:
                if convert_to_mp3(audio_file):
                    successful_conversions += 1
                    mp3_file = f"{os.path.splitext(audio_file)[0]}.mp3"
                    session['processed_files'].append(mp3_file)
                successful_downloads += 1

        create_summary_report(total_videos, videos_to_process, successful_downloads, successful_conversions, primary_query, secondary_query, upload_date, duration)

    thread = threading.Thread(target=process_in_background)
    thread.start()
    return jsonify({"message": "Processing started. Check console for progress."})

@app.route('/download_zip', methods=['GET'])
def download_zip():
    processed_files = session.get('processed_files', [])
    
    if not processed_files:
        return jsonify({"error": "No files were processed in the current session."}), 400

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in processed_files:
            if os.path.exists(file):
                zf.write(file, os.path.basename(file))
    memory_file.seek(0)
    return send_file(memory_file, download_name='processed_audio.zip', as_attachment=True)

@app.route('/test_search', methods=['POST'])
def test_search():
    primary_query = request.form['primary_query']
    secondary_query = request.form['secondary_query']
    limit = int(request.form['limit'])
    upload_date = request.form['upload_date']
    duration = request.form['duration']
    num_searches = int(request.form.get('num_searches', 2))

    results = []
    for i in range(num_searches):
        logging.info(f"Running search {i+1} of {num_searches}")
        total_videos, videos = search_youtube(primary_query, secondary_query, limit, upload_date, duration)
        
        filtered_videos = []
        for video in videos:
            filtered_video = {
                'title': video['title'],
                'link': video['link'],
                'duration': video['duration'],
                'views': video['views'],
                'publish_time': video['publish_time'],
                'channel': video['channel'],
                'score': video['score'],
                'description': video['description'][:200] + '...' if len(video['description']) > 200 else video['description']
            }
            filtered_videos.append(filtered_video)
        
        results.append({
            "search_number": i+1,
            "total_videos": total_videos,
            "videos_found": len(videos),
            "videos": filtered_videos
        })

    return jsonify({
        "message": "Test searches completed.",
        "results": results,
        "search_parameters": {
            "primary_query": primary_query,
            "secondary_query": secondary_query,
            "limit": limit,
            "upload_date": upload_date,
            "duration": duration
        }
    })

@app.route('/evaluate_search', methods=['POST'])
def evaluate_search():
    primary_query = request.form['primary_query']
    secondary_query = request.form['secondary_query']
    limit = int(request.form['limit'])
    upload_date = request.form['upload_date']
    duration = request.form['duration']

    total_videos, videos = search_youtube(primary_query, secondary_query, limit, upload_date, duration)

    evaluation_results = {
        "total_videos_found": total_videos,
        "videos_returned": len(videos),
        "search_parameters": {
            "primary_query": primary_query,
            "secondary_query": secondary_query,
            "limit": limit,
            "upload_date": upload_date,
            "duration": duration
        },
        "videos": []
    }

    for video in videos:
        video_evaluation = {
            "title": video['title'],
            "score": video['score'],
            "relevance_factors": {
                "title_keywords": sum(1 for keyword in primary_query.lower().split() + secondary_query.lower().split() if keyword in video['title'].lower()),
                "description_keywords": sum(1 for keyword in primary_query.lower().split() + secondary_query.lower().split() if keyword in video['description'].lower()),
                "view_count": video['views'],
                "likes": video['likes'],
                "reputable_channel": video['channel'] in ['Mayo Clinic', 'American Cancer Society', 'National Cancer Institute', 'Memorial Sloan Kettering', 'MD Anderson Cancer Center', 'Dana-Farber Cancer Institute', 'ASCO', 'ESMO', 'Cancer Research UK'],
                "duration": video['duration'],
                "publish_time": video['publish_time']
            }
        }
        evaluation_results["videos"].append(video_evaluation)

    return jsonify(evaluation_results)

@app.route('/download-single', methods=['POST'])
def download_single():
    video_url = request.form['video_url']
    try:
        # Download the audio
        audio_file, video_title = download_audio(video_url, "single_video")
        if audio_file:
            # Convert to MP3
            if convert_to_mp3(audio_file):
                mp3_file = audio_file.replace('.wav', '.mp3')
                return send_file(
                    mp3_file,
                    as_attachment=True,
                    download_name=f"{video_title}.mp3"
                )
            else:
                return jsonify({"error": "Failed to convert audio"}), 500
        else:
            return jsonify({"error": "Failed to download audio"}), 500
    except Exception as e:
        logging.error(f"Error processing single video: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
