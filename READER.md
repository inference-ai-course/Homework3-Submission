# Week 3 Homework Submission – READER  
**MLE in GenAI – Week 3: OpenAI API, .env Credentials, and Simple Chatbot**  
**Author:** Wei Yang  
**Notebook:** `Wei_Yang_week3_submission.ipynb`

---

## 🔍 Overview

This Week 3 homework focuses on using the **OpenAI API in Python**, managing **API credentials safely with `.env`**, and building simple demos for:

- Chat completions (LLM assistant)
- Text Embeddings
- (Optionally) Text-to-Speech (TTS)
- Integration with **LangChain** wrappers

The goal is to ensure that the environment is correctly configured to use OpenAI models and that basic LLM operations (chat, embeddings, simple tools) are working end-to-end.

---

## 🧩 Homework Objectives

The notebook implements the core requirements for Week 3:

### ✔️ 1. API Key Management with `.env`

- Uses a `.env` file to store `OPENAI_API_KEY` securely.
- Loads the key in Python using `python-dotenv` or equivalent.
- Verifies that the key is correctly read by making a simple API call.

### ✔️ 2. OpenAI Client Setup

- Initializes the OpenAI client using the new-style Python SDK, e.g.:

  ```python
  from openai import OpenAI
  client = OpenAI()
✔️ 3. Chat Completion Demo

Implements a chat completion example where the model plays the role of an assistant.

Sends a conversation history (system + user messages) and receives model responses.

Demonstrates how to:

Format messages

Control max tokens / temperature

Inspect and print the response text

✔️ 4. Embeddings Demo

Calls the OpenAI embeddings endpoint with a short list of texts.

Extracts the embedding vectors from the response.

Optionally prints:

Embedding length / dimensionality

Example slice of the vector

Discusses possible uses (e.g., similarity search, retrieval, clustering).

✔️ 5. (Optional) Text-to-Speech (TTS) Demo

Uses the TTS endpoint (if enabled in environment).

Converts a short text to audio.

Explains how the audio could be saved or played locally.

✔️ 6. LangChain Integration (Optional / Bonus)

Demonstrates using OpenAI models through LangChain or a similar abstraction.

Wraps the model in a LangChain LLM or ChatModel interface.

Shows a simple chain or pipeline (e.g., prompt template → LLM → output).

📂 Notebook Structure
Section	Description
Environment Setup	Imports, .env loading, OpenAI client initialization
Sanity Check API Call	Verifies the API key works by sending a test prompt
Chat Completion Example	Simple chatbot-style interaction using messages
Embeddings Example	Calls embeddings endpoint and inspects vector output
(Optional) TTS Demo	Text-to-speech request and result handling
LangChain Wrappers	Using OpenAI via LangChain interfaces (if included)
Summary	What was verified and how it supports later weeks
🛠️ How to Run This Notebook

Create/Update .env File

In the same directory as the notebook, create a file named .env with:

OPENAI_API_KEY=your_api_key_here


Install Dependencies (if needed)

In your course environment (e.g. mle_genai):

pip install openai python-dotenv langchain


Activate Environment and Launch Jupyter

conda activate mle_genai
jupyter notebook


Open Wei_Yang_week3_submission.ipynb and run all cells in order.

✅ Results

Running this notebook confirms:

The OpenAI API is correctly configured with .env credentials.

Chat completion calls work and return coherent responses.

Embeddings can be generated and inspected.

(If included) TTS calls function correctly.

The environment is ready for:

RAG systems (Week 4+)

Hybrid retrieval

More advanced LLM tools and pipelines.

This completes the Week 3 homework requirements and sets up a solid foundation for later RAG and retrieval-augmented generation work.
