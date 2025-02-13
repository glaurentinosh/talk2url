from fastapi import FastAPI, HTTPException
import requests
import json
import uuid  # For generating unique session IDs
from transformers import pipeline
from bs4 import BeautifulSoup
import os
import torch
import nltk
from nltk.tokenize import sent_tokenize
from functools import lru_cache

# Fix potential Torch path issue
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

@lru_cache(maxsize=1)
def load_qa_pipeline():
    """Loads the QA model (DeBERTa-v3-large) and caches it in memory."""
    return pipeline("question-answering", model="microsoft/deberta-v3-large")

qa_pipeline = load_qa_pipeline()  # Cached model

# File to store indexed content
INDEX_FILE = "indexed_content.json"

def load_indexed_content():
    """Loads indexed content from a JSON file."""
    try:
        with open(INDEX_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_indexed_content(data):
    """Saves indexed content to a JSON file."""
    with open(INDEX_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load existing indexed content
indexed_content = load_indexed_content()

# Store chat history for multiple sessions
chat_sessions = {}

app = FastAPI()

@app.post("/index/")
def index_url(url: str):
    """Fetches and stores cleaned webpage content."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = ' '.join([p.get_text() for p in soup.find_all("p")])
            sentences = sent_tokenize(text)  # Break into sentences
            indexed_content[url] = " ".join(sentences[:100])  # Store first 100 sentences
            save_indexed_content(indexed_content)
            return {"status": "success", "message": "Indexing successful!"}
        else:
            return {"status": "error", "message": "Failed to fetch the URL."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/start_chat/")
def start_chat():
    """Creates a new chat session."""
    session_id = str(uuid.uuid4())  # Generate unique session ID
    chat_sessions[session_id] = []  # Initialize empty conversation history
    return {"status": "success", "session_id": session_id}

@app.post("/ask/")
def ask(url: str, question: str, session_id: str):
    """Answers a question with chat history support."""
    if url not in indexed_content:
        return {"status": "error", "message": "URL not indexed yet. Please index it first."}
    
    if session_id not in chat_sessions:
        return {"status": "error", "message": "Invalid session ID. Start a new chat session first."}

    # Get previous chat history
    chat_history = chat_sessions[session_id]

    # Combine previous questions and answers for better context
    context = indexed_content[url] + " " + " ".join(chat_history[-5:])  # Last 5 messages

    # Get the answer from the model
    result = qa_pipeline(question=question, context=context)
    answer = result['answer']

    # Save question and answer to session
    chat_sessions[session_id].append(f"Q: {question}")
    chat_sessions[session_id].append(f"A: {answer}")

    return {"status": "success", "answer": answer, "chat_history": chat_sessions[session_id]}

# run in terminal uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
