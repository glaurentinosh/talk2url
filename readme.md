# Talk2url project

This project is a **Web Q&A Chatbot** that allows users to **index web pages** and **ask questions** about their content. It supports **follow-up questions** using session-based chat history.

## 🚀 Features
- **Web Scraping & Indexing**: Extracts text from web pages.
- **Question Answering**: Uses a pre-trained **BERT QA model**.
- **Follow-up Questions**: Maintains chat history per session.
- **Streamlit Frontend**: Interactive UI.
- **FastAPI Backend**: Handles requests efficiently.

## 🏗️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Machine Learning**: [Hugging Face Transformers](https://huggingface.co/)
- **Web Scraping**: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## 📥 Installation
### 1️⃣ Clone the Repository
```bash
git clone git@github.com:glaurentinosh/talk2url.git
cd talk2url
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

---

## 🏃 Run the Application
### **1️⃣ Start the FastAPI Backend**
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

### **2️⃣ Start the Streamlit Frontend**
```bash
streamlit run app.py
```

---

## 📌 API Endpoints
### **1️⃣ Index a Web Page**
```http
POST /index/
```
**Params:** `url` (string)

### **2️⃣ Start a New Chat Session**
```http
POST /start_chat/
```
**Response:** `{ session_id: "unique-id" }`

### **3️⃣ Ask a Question**
```http
POST /ask/
```
**Params:** `url` (string), `question` (string), `session_id` (string)

---

## 🛠️ Customization
- Change the **number of stored chat messages** in `backend.py`:
  ```python
  context = indexed_content[url] + " " + " ".join(chat_history[-5:])  # Last 5 messages
  ```
- Modify the **QA model** in `backend.py`:
  ```python
  @st.cache_resource
  def load_qa_pipeline():
      return pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
  ```