from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load token from environment variable for security
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set. Please set it in .env file or as environment variable.")

client = InferenceClient(token=HF_TOKEN)

def generate_response(text: str) -> str:
    try:
        # chat completion API
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": text}],
            max_tokens=200
        )
        # response is ChatCompletionOutput object
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message["content"]
        else:
            return str(response)
    except Exception as e:
        return f"Error generating response: {str(e)}"
