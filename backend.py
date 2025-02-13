from fastapi import FastAPI
import requests
import json
from transformers import pipeline
from bs4 import BeautifulSoup
import os
import torch
import nltk
from nltk.tokenize import sent_tokenize
from functools import lru_cache

# Fix potential Torch path issue
torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the Question-Answering model
# Caching Model using @lru_cache
@lru_cache(maxsize=1)
def load_qa_pipeline():
    return pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

qa_pipeline = load_qa_pipeline()

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

@app.post("/ask/")
def ask(url: str, question: str):
    """Answers a question based on indexed content."""
    if url not in indexed_content:
        return {"status": "error", "message": "URL not indexed yet. Please index it first."}
    
    context = indexed_content[url]
    result = qa_pipeline(question=question, context=context)
    return {"status": "success", "answer": result['answer']}

# run in terminal with uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
# run in browser with http://localhost:8000/docs