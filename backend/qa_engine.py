import faiss
import ollama
import numpy as np

from sentence_transformers import SentenceTransformer

# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

document_chunks = []

index = None


# -----------------------------------
# Chunk text
# -----------------------------------

def chunk_text(
    text,
    chunk_size=700
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


# -----------------------------------
# Store document
# -----------------------------------

def store_document(text):

    global document_chunks
    global index

    document_chunks = chunk_text(text)

    embeddings = embedding_model.encode(
        document_chunks
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    print("DOCUMENT INDEXED")


# -----------------------------------
# Answer question
# -----------------------------------

def answer_question(question):

    global document_chunks
    global index

    if index is None:

        return "Upload PDF first"

    question_embedding = embedding_model.encode(
        [question]
    )

    question_embedding = np.array(
        question_embedding
    ).astype("float32")

    distances, indices = index.search(
        question_embedding,
        3
    )

    context = ""

    for idx in indices[0]:

        context += (
            document_chunks[idx]
            + "\n"
        )

    prompt = f"""
You are an intelligent PDF QA assistant.

Answer ONLY from context.

Rules:
- Keep answers short
- Do not hallucinate
- If answer unavailable say:
Not available in document

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = ollama.chat(
            model="phi3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return str(e)
