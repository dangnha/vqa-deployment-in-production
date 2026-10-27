"""Streamlit UI: send an image + question to the VQA API and show the answer."""
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000/predict")

st.title("Visual Question Answering")

# Inputs: an image file and a question
uploaded = st.file_uploader("Image", type=["jpg", "jpeg", "png"])
if uploaded is not None:
    st.image(uploaded)
question = st.text_input("Question")

if st.button("Ask"):
    if uploaded is None:
        st.warning("Please upload an image")
    else:
        # POST the image file and the question as multipart form data
        files = {"image": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        resp = requests.post(API_URL, files=files, data={"question": question}, timeout=60)
        body = resp.json()
        # Show the answer on success, the API's error detail otherwise
        if resp.status_code == 200:
            st.success(f"Answer: {body['answer']}")
            st.write(f"Confidence: {body['confidence']:.4f}")
        else:
            st.error(f"Error {resp.status_code}: {body.get('detail')}")
        st.json(body)
