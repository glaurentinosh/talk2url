import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8000"

st.title("Web Q&A App")

# URL Indexing
st.subheader("Step 1: Index a Webpage")
url = st.text_input("Enter URL:")
if st.button("Index URL"):
    response = requests.post(f"{BACKEND_URL}/index/", params={"url": url}).json()
    st.write(response["message"])

# Q&A Section
st.subheader("Step 2: Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Ask"):
    if url:
        response = requests.post(f"{BACKEND_URL}/ask/", params={"url": url, "question": question}).json()
        if response["status"] == "success":
            st.write("Answer:", response["answer"])
        else:
            st.write(response["message"])
    else:
        st.write("Please enter a URL and index it first.")
