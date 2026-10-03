 import truststore
  truststore.inject_into_ssl()
import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from reranker import rerank_documents

load_dotenv()

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please ensure it is set in your .env file.")

genai.configure(api_key=api_key)
llm_model = genai.GenerativeModel('gemini-1.5-pro') # Using Pro for the final synthesis

# Local embedding model (Free!)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def run_query_pipeline(query: str):
    # 1. Stage 1: Candidate Retrieval (Recall)
    print(f"\n--- Stage 1: Vector Search ---")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="legacy_code")

    query_embedding = embed_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20
    )

    candidates = []
    for i in range(len(results['documents'][0])):
        candidates.append({
            "content": results['documents'][0][i],
            "metadata": results['metadatas'][0][i]
        })

    print(f"Retrieved {len(candidates)} candidates from vector store.")

    # 2. Stage 2: Reranking (Precision)
    print(f"\n--- Stage 2: Gemini Reranking ---")
    top_docs = rerank_documents(query, candidates)

    # 3. Final Generation
    print(f"\n--- Final Answer Generation ---")
    context = "\n\n".join([f"File: {d['metadata']['file']}\n{d['content']}" for d in top_docs])

    final_prompt = f"""You are an expert software engineer. Use the following retrieved code snippets to answer the user's question.
If the answer isn't in the code, say "I don't know".
Always cite the filename in your answer.

Context:
{context}

Question: {query}
Answer:"""

    response = llm_model.generate_content(final_prompt)

    return response.text

if __name__ == "__main__":
    user_query = "How is the tax calculated and where is it used?"
    answer = run_query_pipeline(user_query)
    print("\n====================================")
    print(f"QUERY: {user_query}")
    print(f"FINAL ANSWER:\n{answer}")
    print("====================================")
