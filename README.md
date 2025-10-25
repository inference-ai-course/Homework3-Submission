## Building a voice agent

An exciting assignment on building a voice agents.

We start by building the interface, which uses the Fast API library to create `post` API endpoint `/chat/` that accepts an audio file

You can use [Postman](https://www.postman.com/downloads/) to test this out.

---

### Running the project locally

To run the project locally we need to start a server using `uvicorn`

``` bash
uvicorn main:app --reload
```

---

### Transcription

I transcribed my audio using the [openai-whisper](https://github.com/openai/whisper?tab=readme-ov-file) library

---

### LLM

Using huggingface [Transformers](https://huggingface.co/docs/transformers/en/installation) library

Note: I decided to use a local lightweight llm, Ollama


### TTS

[Index TTS2](https://github.com/index-tts/index-tts)

[PYTTSX3](https://pypi.org/project/pyttsx3/)

[Bento TTS](https://github.com/bentoml/BentoXTTS)

``` bash
git clone https://github.com/index-tts/index-tts.git && cd index-tts
git lfs pull  # download large repository files
```

### Dependencies

Found in the `requirements.txt` file.