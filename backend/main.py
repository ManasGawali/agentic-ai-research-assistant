from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from agent import ask_gemini
from pdf_reader import extract_text_from_pdf, chunk_text
from vector_store import create_embeddings, create_faiss_index, search_index
from agents import research_agent, summary_agent, paper_info_agent, router_agent

app = FastAPI()

vector_index = None
document_chunks = None
chat_history = []


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Agentic AI Research Assistant"}


@app.post("/ask")
def ask(q: Question):
    answer = ask_gemini(q.question)
    return {"answer": answer}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global vector_index
    global document_chunks

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_location)

    document_chunks = chunk_text(text)

    embeddings = create_embeddings(document_chunks)

    vector_index = create_faiss_index(embeddings)

    return {
        "chunks_created": len(document_chunks),
        "vector_dimension": embeddings.shape[1]
    }


@app.post("/ask_pdf")
def ask_pdf(q: Question):

    global vector_index
    global document_chunks

    relevant_chunks = search_index(vector_index, document_chunks, q.question)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
Answer the question using the provided document context.

Context:
{context}

Question:
{q.question}
"""

    answer = ask_gemini(prompt)

    return {
        "answer": answer,
        "sources": relevant_chunks
    }

@app.post("/summary")
def summarize_pdf():

    global document_chunks

    if document_chunks is None:
        return {"error": "No PDF uploaded yet"}

    text = "\n".join(document_chunks[:10])

    prompt = f"""
        Summarize the following research paper clearly.

        {text}
    """

    answer = ask_gemini(prompt)

    return {"summary": answer}

@app.post("/paper_info")
def paper_info():

    global document_chunks

    if document_chunks is None:
        return {"error": "No PDF uploaded yet"}

    text = "\n".join(document_chunks[:5])

    prompt = f"""
        From the following research paper extract:

        1. Title
        2. Authors
        3. Main contribution

        {text}
    """

    answer = ask_gemini(prompt)

    return {"paper_info": answer}

@app.post("/agent")
def agent(q: Question):

    global document_chunks
    global vector_index

    route = router_agent(q.question)

    if "summary" in route:
        text = "\n".join(document_chunks[:10])
        result = summary_agent(text)

    elif "paper_info" in route:
        text = "\n".join(document_chunks[:5])
        result = paper_info_agent(text)

    else:
        def search_fn(question):
            return search_index(vector_index, document_chunks, question)

        history_context = "\n".join(chat_history[-4:])

        combined_query = f"""
            Conversation history:
            {history_context}

            User question:
            {q.question}
        """

        result = research_agent(combined_query, search_fn)

        chat_history.append(f"User: {q.question}")
        chat_history.append(f"AI: {result}")

    return {
        "agent_route": route,
        "result": result
    }