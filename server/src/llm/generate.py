import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")

model_name = "mosaicml/mpt-7b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", dtype=torch.float16)

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

def generate_response(user_text):
    conversation_history.append({"role": "user", "content": user_text})
    # Construct prompt from history
    prompt = ""
    for msg in conversation_history:
        print(msg)
        if msg["role"] == "system":
            prompt += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"

    prompt += "Assistant: "
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    conversation_history.append({"role": "assistant", "text": generated_text})
    print(conversation_history)
    return generated_text