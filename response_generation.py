import torch
from transformers import pipeline

llm = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", device="mps", dtype=torch.float16)      

conversation_history = []

def generate_response(user_text):
    conversation_history.append({"role": "user", "text": user_text})
    # Construct prompt from history
    prompt = ""
    for turn in conversation_history[-5:]:
        prompt += f"{turn['role']}: {turn['text']}\n"
    outputs = llm(prompt, max_new_tokens=100)
    bot_response = outputs[0]["generated_text"]
    conversation_history.append({"role": "assistant", "text": bot_response})
    return bot_response