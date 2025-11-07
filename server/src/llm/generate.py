from ollama import Client

client = Client(host='http://localhost:11434')  # or remote endpoint if cloud-based

model_name = "gpt-oss:20b-cloud"

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant. Your responses will be used for TTS as a live conversation, so keep your responses short. The user will not be able to see any visuals or read any latex/math. Respond in one sentence."},
]

def generate_response(user_text):
    conversation_history.append({"role": "user", "content": user_text})

    response = client.chat(model=model_name, messages=conversation_history, options={
        "max_output_tokens": 100
    })

    generated_text = response["message"]["content"]

    conversation_history.append({"role": "assistant", "content": generated_text})

    return generated_text