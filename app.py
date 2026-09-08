import os
import tempfile
import streamlit as st

from src.loader import load_documents
from src.embeddings import get_embedding_model
from src.llm import get_llm
from src.router import build_agentic_query_engine

st.set_page_config(page_title="Agentic RAG", page_icon="🤖")
st.title("🤖 Agentic RAG")
st.caption("LlamaIndex + Gemini + Hugging Face Embeddings — with smart query routing")

if not os.environ.get("GEMINI_API_KEY"):
    st.warning(
        "GEMINI_API_KEY is not set in this environment. "
        "Set it before running: `export GEMINI_API_KEY='your-api-key'`",
        icon="⚠️",
    )

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    if "query_engine" not in st.session_state or st.session_state.get("_file_name") != uploaded_file.name:
        with st.spinner("Indexing document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            documents = load_documents(tmp_path)
            embed_model = get_embedding_model()
            llm = get_llm()

            st.session_state.query_engine = build_agentic_query_engine(
                documents, llm, embed_model
            )
            st.session_state._file_name = uploaded_file.name

    st.success("Document indexed. Ask a question below.")

    query = st.text_input("Ask a question about the document")
    if query:
        with st.spinner("Thinking..."):
            response = st.session_state.query_engine.query(query)
        st.subheader("📌 Answer")
        st.write(str(response))

        with st.expander("Which strategy did the agent pick?"):
            selector_result = getattr(response, "metadata", {}) or {}
            st.json(selector_result if selector_result else {"info": "Not exposed by this response type."})
