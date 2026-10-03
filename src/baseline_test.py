import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please ensure it is set in your .env file.")

client = OpenAI(api_key=api_key)

def get_embedding(text):
    text = text.replace("\\n", " ")
    return client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

def test_retrieval(query):
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="legacy_code")

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    return results

if __name__ == "__main__":
    query = "How is tax calculated?"
    print(f"Query: {query}")

    res = test_retrieval(query)

    if res['documents']:
        print("\n--- Top Result ---")
        print(res['documents'][0][0])
        print("\nMetadata:", res['metadatas'][0][0])
    else:
        print("No results found.")
