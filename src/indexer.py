try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from parser import extract_code_blocks

load_dotenv()

# Local embedding model (FREE - No API key needed!)
# This matches the model used in evaluator.py
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # Local embedding generation
    return model.encode(text).tolist()

def index_codebase(directory):
    print("Extracting code blocks...")
    documents = extract_code_blocks(directory)

    # Use absolute path for the database to avoid CWD issues
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "chroma_db")

    chroma_client = chromadb.PersistentClient(path=db_path)

    try:
        chroma_client.delete_collection(name="legacy_code")
    except:
        pass

    collection = chroma_client.create_collection(name="legacy_code")

    print(f"Indexing {len(documents)} blocks using LOCAL Sentence-Transformers...")

    for doc in documents:
        embedding = get_embedding(doc["content"])

        collection.add(
            ids=[doc["id"]],
            embeddings=[embedding],
            metadatas=[doc["metadata"]],
            documents=[doc["content"]]
        )

    print("Indexing complete. Database saved to:", db_path)

if __name__ == "__main__":
    index_codebase("dummy_codebase")
