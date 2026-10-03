import os
import ssl
import json
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
from mock_llm import mock_llm

# SSL Bypass
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def simple_keyword_search(query, collection):
    """
    FUZZY Keyword Search.
    Looks for any part of the query words inside the code.
    """
    all_docs = collection.get()
    candidates = []

    # Normalize query: lower case and split into words
    query_words = query.lower().replace("?", "").replace(".", "").split()
    # Only keep meaningful words (longer than 3 chars)
    keywords = [w for w in query_words if len(w) > 3]

    print(f"Searching for keywords: {keywords}")

    for i in range(len(all_docs['documents'])):
        doc_text = all_docs['documents'][i].lower()

        # FUZZY MATCH: If any keyword is a SUBSTRING of the code
        # (e.g. 'calculate' matches 'calculate_tax')
        if any(kw in doc_text for kw in keywords):
            candidates.append({
                "id": all_docs['ids'][i],
                "content": all_docs['documents'][i],
                "metadata": all_docs['metadatas'][i]
            })

    return candidates

def run_eval():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_cases_path = os.path.join(base_dir, "test_cases.json")

    if not os.path.exists(test_cases_path):
        print(f"❌ ERROR: Could not find test_cases.json")
        return

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    db_path = os.path.join(base_dir, "chroma_db")
    chroma_client = chromadb.PersistentClient(path=db_path)

    try:
        collection = chroma_client.get_collection(name="legacy_code")
    except Exception as e:
        print(f"❌ ERROR: Could not load collection. \n{e}")
        return

    hits = 0
    total = len(test_cases)

    print(f"Running EVALUATION with Fuzzy Keyword Search on {total} test cases...\n")

    for i, case in enumerate(test_cases):
        query = case["question"]
        expected_id = case["expected_chunk_id"]

        candidates = simple_keyword_search(query, collection)

        # DEBUG: See what was found
        print(f"Found {len(candidates)} candidates for query: {query}")

        # Rerank with Gemini
        top_docs = mock_llm.rerank(query, candidates)
        top_ids = [d["id"] for d in top_docs]

        is_hit = expected_id in top_ids
        if is_hit:
            hits += 1

        status = "✅ HIT" if is_hit else "❌ MISS"
        print(f"Case {i+1}: {status} | Expected: {expected_id}")

    hit_rate = (hits / total) * 100
    print("\n" + "="*30)
    print(f"FINAL EVALUATION REPORT (Fuzzy-Hybrid)")
    print(f"Total Cases: {total}")
    print(f"Hits: {hits}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print("="*30)

if __name__ == "__main__":
    run_eval()
