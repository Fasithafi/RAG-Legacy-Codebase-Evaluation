import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback to a dummy for safety, but we'll warn the user
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env. Reranker will act as a pass-through.")
    genai.configure(api_key="dummy")
else:
    genai.configure(api_key=api_key)

# We use Flash for reranking because it's fast and efficient
model = genai.GenerativeModel('gemini-1.5-flash')

class MockLLM:
    """
    Now upgraded from a 'Mock' to a 'Real' Reranker using Gemini.
    We keep the name MockLLM to avoid changing imports in other files.
    """
    def rerank(self, query, documents):
        if not documents:
            return []

        print(f"[GeminiReranker] Evaluating {len(documents)} candidates...")

        relevant_docs = []

        for doc in documents:
            prompt = f"""You are a technical code expert.
Determine if the following code block is directly relevant to answering the user query.
Answer ONLY 'YES' or 'NO'.

Query: {query}
Code:
{doc['content']}

Is this code relevant? """

            try:
                response = model.generate_content(prompt)
                decision = response.text.strip().upper()
                if "YES" in decision:
                    relevant_docs.append(doc)
            except Exception as e:
                # On API error, we keep the doc to avoid losing potential hits
                relevant_docs.append(doc)

        print(f"[GeminiReranker] Kept {len(relevant_docs)} relevant documents.")
        return relevant_docs

    def generate(self, query, context):
        # Final synthesis using Gemini
        prompt = f"""You are an expert software engineer. Use the following retrieved code snippets to answer the user's question.
If the answer isn't in the code, say "I don't know".
Always cite the filename in your answer.

Context:
{context}

Question: {query}
Answer:"""

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {e}"

# Global instance
mock_llm = MockLLM()
