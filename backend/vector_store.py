import faiss
import numpy as np
from vertexai.language_models import TextEmbeddingModel

model = TextEmbeddingModel.from_pretrained("text-embedding-005")

def create_embeddings(chunks, batch_size=25):

    all_embeddings = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        response = model.get_embeddings(batch)

        embeddings = [r.values for r in response]

        all_embeddings.extend(embeddings)

    return np.array(all_embeddings).astype("float32")


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_index(index, chunks, question, top_k=5):

    q_embedding = model.get_embeddings([question])[0].values
    q_embedding = np.array([q_embedding]).astype("float32")

    distances, indices = index.search(q_embedding, top_k)

    results = [chunks[i] for i in indices[0]]

    return results