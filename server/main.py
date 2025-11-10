from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import whisper
import sys
sys.path.append('third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import CosyVoice, CosyVoice2
from cosyvoice.utils.file_utils import load_wav
import torchaudio
from ollama import chat, ChatResponse
    

app = FastAPI()

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    # ASR
    user_text = transcribe_audio(audio_bytes)
    print(f'********user_text: {user_text}')

    # LLM
    bot_text = generate_response(user_text)
    print(f'********bot_text: {bot_text}')

    # TTS
    audio_path = synthesize_speech(bot_text)

    return FileResponse(audio_path, media_type="audio/wav")


asr_model = whisper.load_model("small")

def transcribe_audio(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = asr_model.transcribe("temp.wav", fp16=False)
    return result["text"]


conversation_history = []

def generate_response(user_text):
    conversation_history.append({"role": "user", "content": user_text})
    messages = conversation_history[-5:]
    print(f'********messages: {messages}')
    response: ChatResponse = chat(
        model='llama3',
        messages=messages,
        options={'num_predict': 50}
    )
    bot_response = response['message']['content']
    conversation_history.append({"role": "assistant", "content": bot_response})
    return bot_response


cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B', load_jit=False, load_trt=False, load_vllm=False, fp16=False)

def text_generator(bot_text):
    '''
    for sentence in bot_text.split('.'):
        yield sentence'''
    yield bot_text


def synthesize_speech(bot_text):
    prompt_speech_16k = load_wav('./asset/zero_shot_prompt.wav', 16000)
    for i, j in enumerate(cosyvoice.inference_zero_shot(text_generator(bot_text), '', prompt_speech_16k, stream=False)):
        torchaudio.save('zero_shot_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)
    return 'zero_shot_0.wav'