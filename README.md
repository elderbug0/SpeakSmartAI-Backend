

# Public Speaking Video Analysis Backend

## Overview

This is a Flask-based backend of Speak Smart Ai project. Check frontend on https://github.com/elderbug0/SpeakSmartAI-Frontend . Users upload their videos, and the system extracts audio, analyzes speech, and provides feedback using the OpenAI API (GPT-4o) and Gemini API for detailed video analysis. The feedback includes sentiment analysis, clarity, tone, grammar, engagement, and speaker body language assessment.

### Features

- **Video and Audio Processing**: Users can upload videos, and the system extracts the audio for speech-to-text conversion.
- **GPT-4o Analysis**: The extracted text is analyzed using GPT-4o for public speaking feedback.
- **Gemini Video Analysis**: Uploaded videos are analyzed for body language feedback using Gemini API.
- **Language Support**: Currently supports English (`en`) and can be extended for other languages.
- **Error Logging and Status Tracking**: Logs any errors encountered during video/audio processing and tracks the status of each request.

## Project Structure

```bash
├── app.py                 # Main application file
├── audio
│   ├── audio_controller.py # Handles audio-related endpoints
│   ├── audio_routes.py     # Defines audio routes for the Flask app
│   ├── audio_service.py    # Services for handling audio processing & GPT-4o requests
├── video
│   ├── video_controller.py # Handles video-related endpoints
│   ├── video_routes.py     # Defines video routes for the Flask app
│   ├── video_service.py    # Services for handling video processing & Gemini API requests
├── global_router.py        # Registers all routes
├── logger.py               # Logs incoming requests
├── requirements.txt        # Project dependencies
└── README.md               # Documentation (this file)
```

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Flask
- MoviePy
- Requests
- OpenAI Python SDK
- Google Gemini SDK

### Clone the Repository


git clone https://github.com/your-repo/public-speaking-analysis.git
cd public-speaking-analysis


### Install Dependencies


pip install -r requirements.txt


### Setup Environment Variables

Create a `.env` file in the project root and add the following keys:


OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
AUTH_TOKEN=your_auth_token_for_edenai


### Run the Application


python app.py


The application will start on `http://localhost:8000`.

## API Endpoints

### 1. Upload Video for Audio Analysis

**Endpoint**: `/api/v1/audio/upload`  
**Method**: POST  
**Description**: Uploads a video, extracts audio, and provides GPT-4o feedback on the speech content.

**Request Body**:
- `video`: File (MP4)
- `language`: Optional (default: `en`)

**Response**:
- `200 OK`: JSON with speech analysis results.
- `400 Bad Request`: Error details if the video file is missing.
- `500 Internal Server Error`: Error during file processing or analysis.
