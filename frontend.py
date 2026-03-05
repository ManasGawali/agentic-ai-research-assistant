import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📚 Agentic AI Research Assistant")

# Upload PDF
uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("PDF uploaded and processed!")

# Ask Question
question = st.text_input("Ask a question about the paper")

if st.button("Ask AI"):
    response = requests.post(
        f"{API_URL}/agent",
        json={"question": question}
    )

    data = response.json()

    st.subheader("AI Answer")
    st.write(data["result"])

    st.caption(f"Agent used: {data['agent_route']}")