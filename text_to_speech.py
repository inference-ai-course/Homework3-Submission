from gtts import gTTS

def synthesize_speech(text):
    tts = gTTS(text)
    tts.save('zero_shot.wav')
    