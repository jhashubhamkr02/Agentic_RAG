# Agentic RAG

An Agentic Retrieval-Augmented Generation (RAG) system built with **LlamaIndex**, **Gemini**, and **Hugging Face embeddings**. Instead of a fixed retrieve-then-generate pipeline, an LLM-driven router decides — per query — whether to run vector retrieval (for specific, fact-based questions) or a summarization pass (for broad, whole-document questions).

## Features
- **Smart Query Handling** — an `LLMSingleSelector` picks between a vector retrieval engine and a summarization engine based on the query itself.
- **Better Efficiency** — narrow questions skip full-document summarization.
- **Higher Adaptability** — broad "summarize this" questions get a tree-summarize pass instead of a handful of possibly-irrelevant chunks.
- **Improved Accuracy** — matching retrieval strategy to query type reduces the chance of answering from the wrong context.

## Tech Stack
- **LlamaIndex** — document indexing, vector + summary indices, query routing
- **Gemini API** (`gemini-2.0-flash` via `llama-index-llms-google-genai`) — generation and route selection
- **Hugging Face `sentence-transformers/all-MiniLM-L6-v2`** — embeddings
- **Streamlit** — UI

## Project Structure
```
app.py                  Streamlit UI
src/loader.py            Document loading (PDF/txt/docx)
src/embeddings.py        Hugging Face embedding model
src/llm.py                Gemini LLM wrapper
src/router.py             Agentic RouterQueryEngine (vector vs. summary)
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set your Gemini API key (get one from Google AI Studio):

```bash
export GEMINI_API_KEY='your-api-key'
```

## Run

```bash
streamlit run app.py
```

Upload a PDF, then ask a question. Try one narrow question ("What does X say about Y?") and one broad question ("Summarize this document") to see the router pick different strategies — expand the "Which strategy did the agent pick?" panel under the answer.
