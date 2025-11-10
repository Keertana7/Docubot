import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === Load your raw dataset ===
with open("ceph_docs_dataset.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# === Step 1: Deep clean the text ===
def advanced_clean(text):
    # Remove code blocks, directives, etc.
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\.\.\s+\w+::", "", text)   # remove sphinx directives like .. note::
    text = re.sub(r"::", "", text)
    text = re.sub(r"\s+", " ", text)           # collapse multiple spaces/newlines
    text = text.replace("¶", "").strip()
    return text

# === Step 2: Extract section name ===
def extract_section(content, file_name):
    """
    Try to extract the main section title from the .rst content.
    Fallback: use file name if section header not found.
    """
    # Match patterns like:
    # Title
    # =====
    match = re.search(r"^([A-Za-z0-9 \-_]+)\n[=~\-]{3,}\n", content, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        return file_name.split("/")[-1].replace(".rst", "").replace("_", " ").title()

cleaned_data = []
for entry in raw_data:
    content = advanced_clean(entry["content"])
    section = extract_section(entry["content"], entry["file"])
    cleaned_data.append({
        "file": entry["file"],
        "section": section,
        "content": content
    })

# === Step 3: Split into ~400–600 word chunks (≈ 2000–2500 characters) ===
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2200,   # target ~400–600 words
    chunk_overlap=300  # small overlap (~50 words)
)

chunked_data = []
for item in cleaned_data:
    chunks = splitter.split_text(item["content"])
    for i, chunk in enumerate(chunks):
        chunked_data.append({
            "file": item["file"],
            "section": item["section"],
            "chunk_id": i + 1,
            "content": chunk,
            "word_count": len(chunk.split())
        })

# === Step 4: Save processed dataset ===
with open("ceph_docs_preprocessed.json", "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, indent=2, ensure_ascii=False)

# === Step 5: Verify average chunk length ===
avg_words = sum(d["word_count"] for d in chunked_data) / len(chunked_data)
print(f"✅ Preprocessing complete!")
print(f"Total chunks created: {len(chunked_data)}")
print(f"Average words per chunk: {avg_words:.0f}")
print("Example chunk with metadata:\n", json.dumps(chunked_data[0], indent=2)[:600])
