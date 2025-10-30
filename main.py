from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import whisper
from transformers import pipeline
from huggingface_hub import login
from TTS.api import TTS
import torch
import os 

device = "cuda" if torch.cuda.is_available() else "cpu"

hf_token = open("../hf_token.txt").read().strip()  
login(token=hf_token)

app = FastAPI()

asr_model = whisper.load_model("small")
llm = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct", device=device)  # ← CHANGED: Added device
conversation_history = []
tts_engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def transcribe_audio(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = asr_model.transcribe("temp.wav")
    os.remove("temp.wav")  
    return result["text"]

def generate_response(user_text):
    conversation_history.append({"role": "user", "content": user_text})
    
    messages = [{"role": msg["role"], "content": msg["content"]} 
                for msg in conversation_history[-10:]]  # Keep last 10 messages
    
    outputs = llm(messages, max_new_tokens=1000, do_sample=True, temperature=0.7)
    bot_response = outputs[0]["generated_text"][-1]["content"]
    conversation_history.append({"role": "assistant", "content": bot_response})
    print(f"Bot: {bot_response}")
    return bot_response

def synthesize_speech(text, filename="./response.wav"):
    tts_engine.tts_to_file(
        text=text,
        file_path=filename,
        speaker="Ana Florence",
        language="en",
        split_sentences=True
    )
    return filename

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        user_text = transcribe_audio(audio_bytes)
        print(f"User: {user_text}") 
        bot_text = generate_response(user_text)
        audio_path = synthesize_speech(bot_text)
        
        return FileResponse(audio_path, media_type="audio/wav")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/history/")
async def get_history():
    """Returns the full conversation history"""
    return JSONResponse({"history": conversation_history})

@app.delete("/history/")
async def clear_history():
    """Clears the conversation history"""
    global conversation_history
    conversation_history = []
    return JSONResponse({"message": "History cleared"})

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Voice Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }
            .controls {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            #recordBtn {
                flex: 1;
                padding: 20px;
                font-size: 18px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            #recordBtn:hover {
                background: #764ba2;
                transform: scale(1.05);
            }
            #recordBtn:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: scale(1);
            }
            #recordBtn.recording {
                background: #e74c3c;
                animation: pulse 1.5s infinite;
            }
            #clearBtn {
                padding: 20px;
                font-size: 16px;
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            #clearBtn:hover {
                background: #c0392b;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            #status {
                margin-top: 20px;
                padding: 15px;
                background: #f0f0f0;
                border-radius: 8px;
                text-align: center;
                min-height: 50px;
                font-weight: bold;
            }
            #chatHistory {
                margin-top: 30px;
                max-height: 400px;
                overflow-y: auto;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
                border: 2px solid #e0e0e0;
            }
            #chatHistory:empty::before {
                content: "No messages yet. Start recording!";
                color: #999;
                font-style: italic;
                display: block;
                text-align: center;
                padding: 40px;
            }
            .message {
                margin: 15px 0;
                padding: 12px 16px;
                border-radius: 10px;
                animation: slideIn 0.3s ease;
                max-width: 80%;
            }
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: auto;
                text-align: right;
                border-bottom-right-radius: 3px;
            }
            .assistant-message {
                background: white;
                color: #333;
                margin-right: auto;
                border: 2px solid #667eea;
                border-bottom-left-radius: 3px;
            }
            .message-label {
                font-size: 11px;
                font-weight: bold;
                margin-bottom: 5px;
                opacity: 0.8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .message-content {
                font-size: 15px;
                line-height: 1.5;
            }
            .scroll-hint {
                text-align: center;
                color: #999;
                font-size: 12px;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎙️ Voice Chatbot</h1>
            
            <div class="controls">
                <button id="recordBtn">Click to Record</button>
                <button id="clearBtn">🗑️ Clear</button>
            </div>
            
            <div id="status">Ready to listen...</div>
            
            <div id="chatHistory"></div>
            <div class="scroll-hint">💬 Your conversation appears here</div>
        </div>

        <script>
            let mediaRecorder;
            let audioChunks = [];
            const recordBtn = document.getElementById('recordBtn');
            const clearBtn = document.getElementById('clearBtn');
            const status = document.getElementById('status');
            const chatHistory = document.getElementById('chatHistory');

            const API_URL = window.location.origin;

            // Load chat history on page load
            loadHistory();

            recordBtn.addEventListener('click', async () => {
                if (!mediaRecorder || mediaRecorder.state === 'inactive') {
                    await startRecording();
                } else {
                    stopRecording();
                }
            });

            clearBtn.addEventListener('click', async () => {
                if (confirm('Are you sure you want to clear the chat history?')) {
                    await clearHistory();
                }
            });

            async function loadHistory() {
                try {
                    const response = await fetch(`${API_URL}/history/`);
                    const data = await response.json();
                    displayHistory(data.history);
                } catch (error) {
                    console.error('Error loading history:', error);
                }
            }

            async function clearHistory() {
                try {
                    const response = await fetch(`${API_URL}/history/`, {
                        method: 'DELETE'
                    });
                    if (response.ok) {
                        chatHistory.innerHTML = '';
                        status.textContent = 'History cleared! Ready for a fresh start.';
                        status.style.color = '#27ae60';
                        setTimeout(() => {
                            status.textContent = 'Ready to listen...';
                            status.style.color = '#333';
                        }, 2000);
                    }
                } catch (error) {
                    console.error('Error clearing history:', error);
                }
            }

            function displayHistory(history) {
                chatHistory.innerHTML = '';
                history.forEach(msg => {
                    addMessageToUI(msg.role, msg.content);
                });
                scrollToBottom();
            }

            function addMessageToUI(role, content) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}-message`;
                
                const label = document.createElement('div');
                label.className = 'message-label';
                label.textContent = role === 'user' ? 'You' : 'Assistant';
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.textContent = content;
                
                messageDiv.appendChild(label);
                messageDiv.appendChild(contentDiv);
                chatHistory.appendChild(messageDiv);
            }

            function scrollToBottom() {
                chatHistory.scrollTop = chatHistory.scrollHeight;
            }

            async function startRecording() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.addEventListener('dataavailable', event => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener('stop', async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        await sendAudioToServer(audioBlob);
                        stream.getTracks().forEach(track => track.stop());
                    });

                    mediaRecorder.start();
                    recordBtn.textContent = '⏹️ Stop Recording';
                    recordBtn.classList.add('recording');
                    status.textContent = '🎤 Recording... Speak now!';
                    status.style.color = '#e74c3c';
                } catch (err) {
                    status.textContent = '❌ Microphone access denied!';
                    status.style.color = '#e74c3c';
                    console.error('Error accessing microphone:', err);
                }
            }

            function stopRecording() {
                mediaRecorder.stop();
                recordBtn.textContent = 'Click to Record';
                recordBtn.classList.remove('recording');
                status.textContent = '⏳ Processing your voice...';
                status.style.color = '#f39c12';
                recordBtn.disabled = true;
            }

            async function sendAudioToServer(audioBlob) {
                const formData = new FormData();
                formData.append('file', audioBlob, 'audio.wav');

                try {
                    const response = await fetch(`${API_URL}/chat/`, {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error('Server error');
                    }

                    // Reload history to show the new messages
                    await loadHistory();

                    const audioResponse = await response.blob();
                    const audioUrl = URL.createObjectURL(audioResponse);
                    const audio = new Audio(audioUrl);
                    
                    status.textContent = '🔊 Playing response...';
                    status.style.color = '#27ae60';
                    
                    audio.play();
                    
                    audio.onended = () => {
                        status.textContent = 'Ready to listen...';
                        status.style.color = '#333';
                        recordBtn.disabled = false;
                    };

                } catch (error) {
                    status.textContent = '❌ Error: ' + error.message;
                    status.style.color = '#e74c3c';
                    recordBtn.disabled = false;
                    console.error('Error:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
