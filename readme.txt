# 🎙️ Voice Agent - Real-Time Voice Assistant

A production-ready voice chatbot that processes audio input, generates intelligent responses using LLM, and returns synthesized speech.

## 📋 Features

- ✅ **Speech-to-Text (ASR)**: OpenAI Whisper for accurate transcription
- ✅ **LLM Response Generation**: Llama 3.2 for natural conversations
- ✅ **Text-to-Speech (TTS)**: Google TTS for natural-sounding audio
- ✅ **5-Turn Conversation Memory**: Context-aware multi-turn dialogues
- ✅ **FastAPI REST API**: Production-ready HTTP interface
- ✅ **Async Processing**: Optimized for low latency
- ✅ **Session Management**: Track multiple concurrent conversations

## 🏗️ Architecture

```
Audio Input → ASR (Whisper) → LLM (Llama) → TTS (gTTS) → Audio Output
                    ↓
            Conversation Memory (5 turns)
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- 4-6GB RAM (8GB recommended)
- 2-3GB disk space for models
- Internet connection (for gTTS)

### Step 1: Clone or Extract Project

```bash
# If using git
git clone <your-repo-url>
cd voice-agent-simple

# Or extract the provided files
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Note**: First install will download model files (~2-3GB). This may take 10-30 minutes.

### Step 4: Create Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (optional)
# Default settings work for most cases
```

### Step 5: Create Required Directories

```bash
# Create data directories
mkdir -p data/temp
mkdir -p logs

# Or on Windows:
# md data\temp
# md logs
```

## 🚀 Running the Application

### Start the Server

```bash
# Run with Python
python main.py

# Or with uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Verify Installation

Open your browser and visit:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📝 Usage

### Using cURL

```bash
# Send audio file
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/audio.wav" \
  --output response.mp3

# With session ID for conversation continuity
curl -X POST "http://localhost:8000/chat/" \
  -H "X-Session-ID: your-session-id" \
  -F "file=@path/to/your/audio.wav" \
  --output response.mp3
```

### Using Python

```python
import requests

url = "http://localhost:8000/chat/"

# Upload audio file
with open("input.wav", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Get session ID from headers
session_id = response.headers.get("X-Session-ID")
transcript = response.headers.get("X-Transcript")
bot_response = response.headers.get("X-Bot-Response")

print(f"You said: {transcript}")
print(f"Bot said: {bot_response}")

# Save audio response
with open("response.mp3", "wb") as f:
    f.write(response.content)

# Continue conversation
with open("input2.wav", "rb") as f:
    files = {"file": f}
    headers = {"X-Session-ID": session_id}
    response = requests.post(url, files=files, headers=headers)
```

### Using Postman

1. Create a new POST request to `http://localhost:8000/chat/`
2. In Body tab, select "form-data"
3. Add key "file" and select your audio file
4. (Optional) Add header "X-Session-ID" for conversation continuity
5. Send request
6. Save response as `.mp3` file

## 🧪 Testing

### Test with Sample Audio

Create a simple test audio:

```python
# test_voice.py
from gtts import gTTS
import requests

# Create test audio
tts = gTTS("Hello, how are you today?", lang='en')
tts.save("test_input.wav")

# Send to API
with open("test_input.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/chat/",
        files={"file": f}
    )

# Check response
print("Status:", response.status_code)
print("Transcript:", response.headers.get("X-Transcript"))
print("Response:", response.headers.get("X-Bot-Response"))

# Save output
with open("test_output.mp3", "wb") as f:
    f.write(response.content)

print("Response saved to test_output.mp3")
```

Run the test:
```bash
python test_voice.py
```

### Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Model Selection
WHISPER_MODEL=small     # Options: tiny, base, small, medium, large
LLM_MODEL=meta-llama/Llama-3.2-1B  # Or Llama-3.2-3B

# Device (CPU or GPU)
WHISPER_DEVICE=cpu      # Use 'cuda' for GPU
LLM_DEVICE=cpu          # Use 'cuda' for GPU

# TTS Settings
TTS_LANGUAGE=en         # Language code
TTS_SLOW=False          # Slow speech for learning

# Conversation
MAX_CONVERSATION_TURNS=5
SESSION_TIMEOUT=3600    # 1 hour

# Files
MAX_FILE_SIZE=10485760  # 10MB
```

## 📊 Performance

### Expected Latency (CPU)

| Component | Time |
|-----------|------|
| ASR (Whisper small) | 2-3s |
| LLM (Llama-3.2-1B) | 3-5s |
| TTS (gTTS) | 1-2s |
| **Total** | **8-10s** |

### With GPU

Enable GPU for 2-3x faster processing:

```bash
# In .env file
WHISPER_DEVICE=cuda
LLM_DEVICE=cuda
```

Expected latency: **3-5s total**

## 🐛 Troubleshooting

### Models Not Downloading

```bash
# Manually download models
python -c "import whisper; whisper.load_model('small')"
python -c "from transformers import AutoModel; AutoModel.from_pretrained('meta-llama/Llama-3.2-1B')"
```

### Out of Memory Error

Try smaller models:
```bash
# In .env
WHISPER_MODEL=tiny
LLM_MODEL=meta-llama/Llama-3.2-1B  # Already smallest
```

### gTTS Network Error

Check internet connection. gTTS requires internet access.

### Port Already in Use

Change port in `.env`:
```bash
API_PORT=8001
```

## 📁 Project Structure

```
voice-agent-simple/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env                     # Configuration
│
├── api/
│   ├── main.py             # FastAPI app
│   ├── routes/
│   │   ├── chat.py         # Chat endpoint
│   │   └── health.py       # Health check
│   ├── middleware/
│   │   └── error_handler.py
│   └── schemas/
│       └── responses.py
│
├── services/
│   ├── asr/
│   │   └── whisper_asr.py  # Speech-to-text
│   ├── llm/
│   │   └── llama_client.py # Response generation
│   ├── tts/
│   │   └── gtts_client.py  # Text-to-speech
│   └── conversation/
│       └── manager.py      # State management
│
├── orchestrator/
│   └── pipeline.py         # Main processing pipeline
│
├── utils/
│   ├── logger.py
│   ├── file_manager.py
│   └── audio_utils.py
│
└── config/
    ├── settings.py
    └── constants.py
```

## 📚 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🎯 Assignment Deliverables

### Required Components ✅

1. **Runnable FastAPI project** ✅
   - `main.py` entry point
   - `/chat/` endpoint working
   - All dependencies in `requirements.txt`

2. **5-turn conversation memory** ✅
   - Session-based tracking
   - Automatic history management
   - Memory pruning

3. **Modular components** ✅
   - ASR service (Whisper)
   - LLM service (Llama)
   - TTS service (gTTS)
   - Clear separation of concerns

4. **Demo recording** 🎥
   - Record 5 turns of interaction
   - Show request/response cycle
   - Demonstrate conversation memory

### Demo Script

```bash
# Turn 1
curl -X POST "http://localhost:8000/chat/" \
  -F "file=@turn1.wav" --output response1.mp3

# Turn 2 (with session ID from turn 1)
curl -X POST "http://localhost:8000/chat/" \
  -H "X-Session-ID: <session-id>" \
  -F "file=@turn2.wav" --output response2.mp3

# Repeat for turns 3, 4, 5...
```

## 🌟 Extension Ideas (Optional)

- [ ] Add database persistence (SQLite/PostgreSQL)
- [ ] Implement streaming responses
- [ ] Add voice activity detection
- [ ] Support multiple languages
- [ ] Add user authentication
- [ ] Deploy with Docker
- [ ] Add monitoring dashboard
- [ ] Implement caching for common queries

## 📄 License

This project is created for educational purposes.

## 🤝 Contributing

This is an assignment project. Feel free to extend it for your portfolio!

## 📞 Support

For issues:
1. Check logs in `logs/voice_agent.log`
2. Review error messages
3. Verify all dependencies installed
4. Check model downloads completed

---

**Built with ❤️ for VicEdu ML/AI Course**
