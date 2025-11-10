import os
import json
import re

# Path to Ceph documentation folder
DOC_PATH = os.path.join(os.getcwd(), "doc")

def clean_text(text):
    """Remove code blocks, directives, and excessive whitespace."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"::", "", text)
    text = re.sub(r"\.\. .*?::.*?\n", "", text)   # remove rst directives
    text = re.sub(r"\s+", " ", text)
    return text.strip()

dataset = []

for root, dirs, files in os.walk(DOC_PATH):
    for file in files:
        if file.endswith(".rst"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    clean_content = clean_text(content)
                    dataset.append({
                        "file": path.replace(os.getcwd(), "").lstrip("\\/"),
                        "content": clean_content
                    })
            except Exception as e:
                print(f"Error reading {path}: {e}")

# Save dataset
output_path = os.path.join(os.getcwd(), "ceph_docs_dataset.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"\n✅ Dataset created successfully: {output_path}")
print(f"Total documents extracted: {len(dataset)}")

