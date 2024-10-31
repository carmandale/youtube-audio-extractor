# YouTube Audio Extractor

A web application that allows users to search YouTube videos and extract their audio in MP3 format. Built with Flask and modern web technologies.

## Features

- Single video audio extraction via URL
- Batch search and download functionality
- Advanced search filters:
  - Upload date
  - Video duration
  - Number of results
- Modern dark mode interface
- Progress tracking for downloads
- Dropbox integration for file storage

## Requirements

- Python 3.11 or higher
- FFmpeg
- Dropbox account and API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/carmandale/youtube-audio-extractor.git
   cd youtube-audio-extractor
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv

   # On Mac/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install FFmpeg:
   ```bash
   # Mac:
   brew install ffmpeg

   # Linux:
   sudo apt-get install ffmpeg

   # Windows:
   # Download from FFmpeg website
   ```

5. Create `.env` file:
   ```bash
   DROPBOX_ACCESS_TOKEN=your_token_here
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

## Configuration

1. Create a Dropbox App:
   - Go to https://www.dropbox.com/developers/apps
   - Click "Create app"
   - Choose "Scoped access"
   - Choose "Full Dropbox" access
   - Generate access token
   - Add token to `.env` file

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open browser and navigate to:
   ```
   http://localhost:5001
   ```

## Development

- The application uses Flask for the backend
- Frontend is built with vanilla JavaScript and CSS
- Files are stored in Dropbox
- Search results are sorted by relevance

## Project Structure

```
youtube-audio-extractor/
├── main.py              # Application entry point
├── app.py              # Flask application
├── audio_downloader.py # Audio download handling
├── youtube_search.py   # YouTube search functionality
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   └── images/        # Image assets
├── templates/         # HTML templates
│   └── index.html     # Main application page
└── .env              # Environment variables
```

## Local Testing

The application can be tested locally with the following features:
- Full search functionality
- Audio extraction and download
- Progress tracking
- Error handling

## Deployment

The application is configured for Vercel deployment:

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Configure Vercel:
   ```bash
   # Add Dropbox token to Vercel secrets
   vercel secrets add dropbox-access-token "your-token-here"
   ```

3. Deploy:
   ```bash
   vercel
   ```

## Environment Variables

Required environment variables:
- `DROPBOX_ACCESS_TOKEN`: Your Dropbox API access token
- `FLASK_ENV`: Set to 'development' for local testing
- `FLASK_DEBUG`: Set to 1 for debug mode

## Error Handling

The application includes comprehensive error handling for:
- Invalid YouTube URLs
- Failed downloads
- Network issues
- API rate limits
- File system operations

## Security Considerations

- API keys are stored in environment variables
- File names are sanitized
- Downloads are streamed to prevent memory issues
- Rate limiting is implemented
- Error messages are sanitized

## Known Limitations

- Maximum video length: 3 hours
- Maximum concurrent downloads: 5
- Rate limits apply to YouTube API
- Some videos may be region-restricted

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Author

Dale Carman

## Support

For support, please open an issue in the GitHub repository.