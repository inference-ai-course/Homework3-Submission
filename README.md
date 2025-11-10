# Voice Assistant - Week 3 Homework

A real-time voice chatbot that handles multi-turn conversations using ASR (Whisper), LLM (LLaMA 3), and TTS (BentoTTS).

## Features

- Speech-to-text transcription using OpenAI Whisper
- Natural language understanding and response generation using LLaMA 3
- Text-to-speech synthesis using BentoTTS
- 5-turn conversation memory
- RESTful API built with FastAPI

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended, but CPU fallback available)
- 16GB+ RAM (for running LLM models)

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up BentoTTS server:

Follow the instructions at [BentoXTTS](https://github.com/bentoml/BentoXTTS) to set up and run the TTS server:

```bash
# Clone BentoXTTS repository
git clone https://github.com/bentoml/BentoXTTS.git
cd BentoXTTS

# Install and run
pip install -r requirements.txt
bentoml serve service:XTTS
```

The BentoTTS server should be running on `http://localhost:3000`.

## Usage

### Start the Voice Assistant Server

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`.

### API Endpoints

#### POST `/chat/`
Main endpoint for voice interaction. Upload an audio file and receive a voice response.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "accept: audio/wav" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@input.wav" \
  --output response.wav
```

**Example using Python:**
```python
import requests

with open("input.wav", "rb") as audio_file:
    response = requests.post(
        "http://localhost:8000/chat/",
        files={"file": audio_file}
    )

with open("response.wav", "wb") as f:
    f.write(response.content)
```

#### GET `/conversation`
View current conversation history and turn count.

```bash
curl http://localhost:8000/conversation
```

#### POST `/reset`
Reset the conversation history.

```bash
curl -X POST http://localhost:8000/reset
```

#### GET `/health`
Check system health and model status.

```bash
curl http://localhost:8000/health
```

## Project Structure

```
.
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── temp_files/            # Temporary audio files (auto-created)
└── Class 3 Homework.ipynb # Assignment instructions
```

## How It Works

1. **Audio Upload**: Client sends audio file via POST request
2. **ASR (Automatic Speech Recognition)**: Whisper transcribes audio to text
3. **LLM Processing**: LLaMA 3 generates a contextual response based on conversation history
4. **TTS (Text-to-Speech)**: BentoTTS converts the response to audio
5. **Audio Response**: Server returns synthesized speech as WAV file

## Configuration

Key configuration variables in `main.py`:

- `MAX_CONVERSATION_TURNS`: Number of conversation turns to remember (default: 5)
- `TEMP_DIR`: Directory for temporary audio files
- Whisper model size: `"small"` (can change to `"base"`, `"medium"`, `"large"`)
- LLM model: `"meta-llama/Llama-3.2-3B-Instruct"` (fallback to 1B if memory limited)

## Troubleshooting

### Out of Memory Error
If you encounter GPU memory issues, the code automatically falls back to a smaller model (Llama-3.2-1B) or CPU mode.

### BentoTTS Connection Error
Make sure the BentoTTS server is running on `http://localhost:3000` before starting the voice assistant.

### Audio Format Issues
Ensure your input audio is in a compatible format (WAV, MP3, etc.). Whisper supports most common audio formats.

## Testing

You can test the API using:
- `curl` commands (see examples above)
- Postman or similar API testing tools
- The Swagger UI at `http://localhost:8000/docs`
- A custom frontend application

## License

See LICENSE file for details.
