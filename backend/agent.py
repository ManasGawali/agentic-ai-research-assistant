import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(
    project="agentic-ai-assistant-489313",
    location="us-central1"
)

model = GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text