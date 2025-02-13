import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "https://talk2url.onrender.com/"

st.title("Web Q&A Chatbot")

# Store session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Step 1: Start a Chat Session
if st.button("Start New Chat"):
    response = requests.post(f"{BACKEND_URL}/start_chat/").json()
    if response["status"] == "success":
        st.session_state.session_id = response["session_id"]
        st.session_state.chat_history = []
        st.write("New chat session started!")
    else:
        st.write("Error starting chat.")

# Step 2: Index a Webpage
st.subheader("Index a Webpage")
url = st.text_input("Enter URL:")
if st.button("Index URL"):
    response = requests.post(f"{BACKEND_URL}/index/", params={"url": url}).json()
    st.write(response["message"])

# Step 3: Ask Questions in Chat Mode
st.subheader("Ask a Question")
question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not st.session_state.session_id:
        st.write("Please start a new chat first.")
    elif url:
        response = requests.post(
            f"{BACKEND_URL}/ask/", 
            params={"url": url, "question": question, "session_id": st.session_state.session_id}
        ).json()
        
        if response["status"] == "success":
            st.session_state.chat_history = response["chat_history"]
            st.write(f"**Answer:** {response['answer']}")
        else:
            st.write(response["message"])

# Display chat history
st.subheader("Chat History")
for msg in st.session_state.get("chat_history", []):
    st.write(msg)
