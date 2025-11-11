# Voice Assistant with Chat History

A voice-based conversational AI assistant that accepts audio input, processes it through ASR (Automatic Speech Recognition), generates responses using an LLM (Large Language Model), converts responses to speech via TTS (Text-to-Speech), and displays the conversation history in a web-based user interface.

## Features

- 🎙️ Voice input via microphone or file upload
- 💬 Multi-turn conversations with 5-turn memory
- 🗣️ Text-to-speech audio responses
- 📜 Visual conversation history display
- 🔄 Real-time chat updates
- 🧹 Clear conversation history option

## Architecture

The system consists of two main components:

1. **FastAPI Backend** (`voice_assistant_api.py`): Handles the ASR → LLM → TTS pipeline
2. **Gradio Frontend** (`voice_assistant_ui.py`): Provides the web UI for interaction

### Technology Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: Gradio
- **ASR**: OpenAI Whisper (small model)
- **LLM**: Ollama with Llama 3.2 1B (local inference)
- **TTS**: pyttsx3
- **Audio Processing**: Standard Python audio libraries

**Note**: The application uses Ollama for local LLM inference. Make sure Ollama is installed and running with the Llama 3.2 1B model before starting the backend.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- **Ollama** installed and running (for LLM inference)
- At least 4GB of RAM (for models)
- Microphone (optional, for voice recording)

### Step 0: Install and Setup Ollama

Before installing the Python dependencies, you need to have Ollama running:

1. **Install Ollama**: Download from https://ollama.ai/download
2. **Pull Llama 3.2 1B model**:
   ```bash
   ollama pull llama3.2:1b
   ```
3. **Verify Ollama is running**:
   ```bash
   ollama run llama3.2:1b
   ```
   Type a test message, then exit with `/bye`

Ollama will continue running in the background and the voice assistant will connect to it automatically.

### Step 1: Clone or Download the Repository

```bash
# If using git
git clone <repository-url>
cd voice-assistant

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- fastapi
- uvicorn
- gradio
- openai-whisper
- pyttsx3
- requests
- python-multipart

**Note**: The first time you run the application, it will download the Whisper model automatically. This may take a few minutes and requires an internet connection. The LLM (Llama 3.2 1B) runs through Ollama, which you should have already set up in Step 0.

### Step 3: Verify Installation

Check that all modules are properly installed:

```bash
python -c "import fastapi, gradio, whisper, transformers, pyttsx3; print('All dependencies installed successfully!')"
```

## Usage

### Starting the Application

You need to start both the backend and frontend servers.

#### Option 1: Using Python Scripts (Cross-platform)

**Terminal 1 - Start Backend:**
```bash
python start_backend.py
```

**Terminal 2 - Start Frontend:**
```bash
python start_frontend.py
```

#### Option 2: Using Batch Files (Windows)

**Terminal 1 - Start Backend:**
```cmd
start_backend.bat
```

**Terminal 2 - Start Frontend:**
```cmd
start_frontend.bat
```

#### Option 3: Manual Start

**Terminal 1 - Start Backend:**
```bash
uvicorn voice_assistant_api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
python voice_assistant_ui.py
```

### Accessing the Application

Once both servers are running:

- **Frontend UI**: Open your browser to `http://127.0.0.1:7860`
- **Backend API**: Available at `http://127.0.0.1:8000`
- **API Documentation**: Visit `http://127.0.0.1:8000/docs` for interactive API docs

### Using the Voice Assistant

1. **Record Audio**: Click the microphone icon to record your voice, or upload an audio file (WAV format recommended)
2. **Send Message**: Click the "Send" button to process your audio
3. **View Response**: The conversation history will update with your transcribed message and the assistant's text response
4. **Listen to Response**: The audio response will play automatically
5. **Continue Conversation**: The assistant remembers the last 5 conversation turns for context
6. **Clear History**: Click "Clear History" to start a new conversation

## Project Structure

```
voice-assistant/
├── asr.py                      # ASR module (Whisper)
├── llm.py                      # LLM module (Llama)
├── tts.py                      # TTS module (pyttsx3)
├── conversation.py             # Conversation manager
├── voice_assistant_api.py      # FastAPI backend
├── voice_assistant_ui.py       # Gradio frontend
├── start_backend.py            # Backend startup script
├── start_frontend.py           # Frontend startup script
├── start_backend.bat           # Windows backend script
├── start_frontend.bat          # Windows frontend script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## API Endpoints

### POST /chat/
Processes audio input and returns audio response.

**Request**: Multipart form data with audio file
**Response**: Audio file (WAV format)

### GET /history
Returns the conversation history.

**Response**: JSON array of conversation turns

### POST /clear
Clears the conversation history.

**Response**: Success message

### GET /health
Health check endpoint.

**Response**: JSON with service status

## Troubleshooting

### Backend Won't Start

**Problem**: `ModuleNotFoundError` or import errors

**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

**Problem**: Port 8000 already in use

**Solution**: 
- Stop any other services using port 8000
- Or modify `start_backend.py` to use a different port (and update `API_URL` in `voice_assistant_ui.py`)

### Frontend Won't Start

**Problem**: Cannot connect to backend

**Solution**:
- Ensure the backend is running first
- Check that backend is accessible at `http://127.0.0.1:8000`
- Verify firewall settings aren't blocking the connection

**Problem**: Port 7860 already in use

**Solution**:
- Stop any other Gradio applications
- Or modify the port in `voice_assistant_ui.py` (line with `ui.launch()`)

### Model Download Issues

**Problem**: Models fail to download on first run

**Solution**:
- Ensure you have a stable internet connection
- Check available disk space (models require ~5GB)
- Try downloading models manually:
```bash
python -c "import whisper; whisper.load_model('small')"
python -c "from transformers import pipeline; pipeline('text-generation', model='distilgpt2')"
```

**Problem**: "Error connecting to Ollama" in responses

**Solution**:
- Ensure Ollama is installed and running
- Check that Ollama is accessible at http://localhost:11434
- Verify the Llama 3.2 1B model is available:
```bash
ollama list
```
- If llama3.2:1b is not listed, pull it:
```bash
ollama pull llama3.2:1b
```
- To use a different Ollama model, update the `model_name` parameter in `llm.py`

**Problem**: "Request timed out" after first message

**Solution**:
- This can happen when conversation history grows and Ollama takes longer to process
- The timeout has been increased to 60 seconds in the latest version
- Try shorter messages or clear the conversation history
- If using a slower machine, consider using a smaller model or reducing `num_predict` in `llm.py`
- Check if Ollama is busy with other requests: `ollama ps`

### Audio Issues

**Problem**: Microphone not working

**Solution**:
- Check browser permissions for microphone access
- Try uploading a pre-recorded audio file instead
- Ensure your microphone is properly connected and configured

**Problem**: No audio playback

**Solution**:
- Check browser audio settings
- Verify speakers/headphones are connected
- Check system volume settings

**Problem**: TTS initialization fails

**Solution**:
```bash
# On Windows, ensure you have the required TTS engines
# On Linux, install espeak:
sudo apt-get install espeak

# On macOS, pyttsx3 should work out of the box
```

### Performance Issues

**Problem**: Slow response times

**Solution**:
- The first request is always slower (model loading)
- Subsequent requests should be faster
- Consider using a smaller Whisper model (change in `asr.py`)
- Ensure you have sufficient RAM (4GB minimum)

**Problem**: Out of memory errors

**Solution**:
- Close other applications to free up RAM
- Use a smaller LLM model if available
- Restart the backend server periodically

### Conversation History Issues

**Problem**: History not displaying correctly

**Solution**:
- Click "Clear History" and start a new conversation
- Refresh the browser page
- Restart both backend and frontend servers

**Problem**: Context not maintained across turns

**Solution**:
- Verify the backend is running continuously
- Check that conversation_manager is properly initialized
- Review backend logs for errors

## Development

### Running in Development Mode

The startup scripts automatically enable reload mode for the backend, which will restart the server when code changes are detected.

### Testing Individual Components

Test ASR module:
```bash
python -c "from asr import transcribe_audio; print('ASR module loaded successfully')"
```

Test LLM module:
```bash
python -c "from llm import generate_response; print('LLM module loaded successfully')"
```

Test TTS module:
```bash
python -c "from tts import synthesize_speech; print('TTS module loaded successfully')"
```

### Logs and Debugging

Backend logs are displayed in the terminal where you started the backend server. Look for:
- Request processing times
- Error messages
- Model loading status

## System Requirements

### Minimum Requirements
- CPU: Dual-core processor
- RAM: 4GB
- Storage: 10GB free space
- OS: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Recommended Requirements
- CPU: Quad-core processor or better
- RAM: 8GB or more
- Storage: 20GB free space (SSD preferred)
- GPU: CUDA-compatible GPU (optional, for faster inference)

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.

## Acknowledgments

- OpenAI Whisper for ASR
- Meta Llama for LLM
- Gradio for the UI framework
- FastAPI for the backend framework
