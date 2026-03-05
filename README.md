# Agentic AI Research Assistant

An AI-powered research assistant that allows users to upload research papers and interact with them using natural language.

Built using Google Vertex AI, Gemini models, and a Retrieval-Augmented Generation (RAG) pipeline.

## Features

- Upload research papers (PDF)
- Ask questions about the document
- Automatic agent routing
- Research paper summarization
- Paper metadata extraction
- Conversational memory
- Vector search using FAISS

## Architecture

User Query  
↓  
FastAPI Backend  
↓  
Router Agent  
↓  
Tool Selection  
- Research QA Agent  
- Paper Summary Agent  
- Paper Metadata Agent  
↓  
Vector Search (FAISS)  
↓  
Gemini via Vertex AI  
↓  
Grounded Response

## Tech Stack

- Python
- FastAPI
- Vertex AI
- Gemini Models
- LangChain
- FAISS
- Streamlit

## Running the Project

### Install dependencies
pip install -r requirements.txt

### Start backend
uvicorn main:app --reload

### Start frontend
streamlit run frontend.py


## Example Use Cases

- Research paper analysis
- Academic literature review
- Knowledge extraction from documents
- AI-assisted research

## Future Improvements

- Multi-document support
- Persistent vector database
- Advanced multi-agent workflows
- Web deployment

