from langchain.agents import Tool
from agent import ask_gemini

def research_agent(question, search_fn):
    chunks = search_fn(question)
    context = "\n\n".join(chunks)

    prompt = f"""
        Answer the research question using this context:

        {context}

        Question:
        {question}
    """

    return ask_gemini(prompt)


def summary_agent(text):
    prompt = f"""
        Summarize this research paper clearly:

        {text}
    """
    return ask_gemini(prompt)


def paper_info_agent(text):
    prompt = f"""
        Extract:
        1. Paper title
        2. Authors
        3. Main contribution

        {text}
    """
    return ask_gemini(prompt)

def router_agent(query):

    prompt = f"""
        Classify the user request into one category:

        research_question → asking about concepts or explanations from the paper
        summary → asking to summarize the paper
        paper_info → asking about title, authors, or metadata

        User request:
        {query}

        Return only one label: research_question, summary, or paper_info.
    """

    return ask_gemini(prompt).strip().lower()