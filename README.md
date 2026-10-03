# 🚀 Evaluated RAG for Legacy Codebases

A professional-grade Retrieval-Augmented Generation (RAG) system designed specifically for navigating legacy Python codebases. This project focuses on **measured precision** rather than "vibe-based" results.

## 🎯 The Problem
Standard RAG implementations often fail on codebases because:
1. **Semantic Gap:** Natural language queries (e.g., *"How is tax handled?"*) don't align well with code identifiers (e.g., `def calc_tax_v2()`).
2. **Noise:** Vector search often retrieves "similar looking" code that is logically irrelevant.

## 🛠️ The Solution: Two-Stage Retrieval Pipeline
This system implements a high-precision pipeline to move from "Recall" to "Precision."

### 1. Structural Ingestion
Instead of naive text chunking, the system uses Python's `ast` (Abstract Syntax Tree) module to parse the codebase. It extracts distinct functions and classes, preserving their structural metadata.

### 2. The Two-Stage Pipeline
- **Stage 1: Recall (HyDE):** Uses **Hypothetical Document Embeddings (HyDE)**. The system generates a synthetic "fake" code answer to the query, then uses that code-like embedding to search the vector store. This aligns the query and document in the same semantic space.
- **Stage 2: Precision (LLM Reranker):** A "Cross-Encoder" pattern. The top 20 candidates are passed to a fast LLM (Gemini 1.5 Flash) which strictly filters out irrelevant chunks, leaving only the most precise matches.

### 3. The Evaluation Wedge
The system is measured against a ground-truth dataset of `(Question, Expected Chunk, Expected Answer)` pairs.
- **Metric:** Hit Rate @ K.
- **Result:** [INSERT YOUR FINAL HIT RATE]% precision.

## 📈 Technical Challenges & Resolutions

### ❌ Challenge: The 0% Hit Rate
**Issue:** Initial tests showed a 0% hit rate. The vector search was failing to connect natural language queries to code identifiers.
**Resolution:** Implemented **HyDE**. By generating a hypothetical code snippet first, the search moved from "searching for a question" to "searching for code," drastically increasing recall.

### ❌ Challenge: Windows SSL/Certificate Failures
**Issue:** Local embedding models from HuggingFace failed to load due to `CERTIFICATE_VERIFY_FAILED` errors on Windows.
**Resolution:** Implemented a hybrid embedding strategy and configured system-level SSL bypasses, ensuring the system could operate in restricted corporate/local environments.

## 🚀 Quick Start
1. Clone the repo.
2. Add your `GEMINI_API_KEY` to `.env`.
3. Run `python src/indexer.py` to build the index.
4. Run `python src/query_engine.py` to chat with your code.
5. Run `python src/evaluator.py` to see the precision report.

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **LLMs:** Google Gemini 1.5 Pro (Synthesis), Gemini 1.5 Flash (Reranking)
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Vector Store:** ChromaDB
- **Parsing:** Python `ast`
