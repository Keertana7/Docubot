# qa_pipeline.py
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import json
import re

def clean_text(text):
    text = text.replace("\n", " ").strip()
    text = re.sub(r":ref:.*?>", "", text)  # remove sphinx refs
    text = re.sub(r"<.*?>", "", text)      # remove any <> tags
    return text

qa_model = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased-distilled-squad"
)

# Load FAISS index
index = faiss.read_index("vector_index.faiss")

# Load mapping from index IDs to chunks
with open("id2chunk.json", "r", encoding="utf-8") as f:
    id2chunk = json.load(f)

# Convert keys to int (JSON saves keys as strings)
id2chunk = {int(k): v for k, v in id2chunk.items()}

# Prepare a list of chunks for easy lookup
doc_chunks = [id2chunk[i] for i in range(len(id2chunk))]


# --------------------------
# Load models
# --------------------------
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# --------------------------
# Conversation Memory
# --------------------------
conversation_history = []  # stores (question, answer) pairs


def build_context(query, history_limit=3):
    """
    Combine recent conversation history with the new query.
    """
    history_text = ""
    for q, a in conversation_history[-history_limit:]:
        history_text += f"Previous Q: {q}\nPrevious A: {a}\n"
    return history_text + f"Now Q: {query}"


# --------------------------
# Query Function
# --------------------------
def answer_query(query, level="Intermediate", top_k=5):
    contextual_query = build_context(query)
    query_vec = embedder.encode([contextual_query])

    # Search FAISS
    D, I = index.search(query_vec, top_k)
    retrieved_chunks = [doc_chunks[i] for i in I[0] if i >= 0]

    # Combine chunks into one context
    context = " ".join(clean_text(chunk) for chunk in retrieved_chunks)

    # Run QA on the combined context
    ans = qa_model(question=query, context=context)
    final_answer = ans['answer'].replace("\n", " ").strip()
    final_answer = re.sub(r"\s+", " ", final_answer)

    # Summarize if answer is long
    if len(final_answer.split()) > 60:
        if level == "Beginner":
            max_len = 60
        elif level == "Intermediate":
            max_len = 120
        else:
            max_len = 200

        summary = summarizer(final_answer, max_length=max_len, min_length=30, do_sample=False)
        final_answer = summary[0]["summary_text"]
        final_answer = re.sub(r"\s+", " ", final_answer).strip()

    conversation_history.append((query, final_answer))
    return final_answer




# --------------------------
# Run as script (for testing)
# --------------------------
if __name__ == "__main__":
    print("🤖 Welcome to DocuBot! Type 'exit' to quit.\n")
    level = input("Choose your level (Beginner/Intermediate/Expert): ")

    while True:
        query = input("Ask a question: ")
        if query.lower() == "exit":
            break
        print("\nAnswer:", answer_query(query, level))
        print("-" * 50)