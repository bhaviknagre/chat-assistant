import streamlit as st
import os
from utils.pipeline import run_pipeline
from utils.document_loader import load_document
from utils.chunks import split_loaded_document
from rag_pipeline.augmentation import augment_question
from rag_pipeline.generation import generate_answer

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="LawAI: Document Indexer & Legal Assistant", layout="wide")

st.title("📚 LawAI: Document Indexer + Legal Q&A Assistant")
tabs = st.tabs(["Document Indexing", "Legal Q&A"])

# --- Document Indexing Tab ---
with tabs[0]:
    st.header("📄 Document Indexer + Embedder with Chroma")
    st.markdown("Upload a document to extract text, split into chunks, generate embeddings, and store with ChromaDB.")
    uploaded_file = st.file_uploader("Upload a document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
    file_path = None
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ File uploaded and saved to `{file_path}`")
    if file_path and st.button("🚀 Run Pipeline"):
        with st.spinner("Running full pipeline (load → chunk → embed → store)..."):
            try:
                run_pipeline(file_path)
                st.success("🎉 Document processed and stored successfully in ChromaDB!")
                try:
                    documents = load_document(file_path)
                    st.subheader("📄 Extracted Document Preview")
                    st.text_area("Full Extracted Text", "\n".join([doc.page_content for doc in documents]), height=300)
                    chunks = split_loaded_document(file_path)
                    st.subheader("📝 First 3 Chunks Preview")
                    for i, chunk in enumerate(chunks[:3]):
                        st.text_area(f"Chunk {i+1}", chunk.page_content, height=150)
                except Exception as e:
                    st.warning(f"⚠️ Unable to preview extracted content after processing: {e}")
            except Exception as e:
                st.error(f"❌ Pipeline failed: {e}")

# --- Legal Q&A Tab ---
with tabs[1]:
    st.header("🤖 Legal AI Assistant")
    st.markdown("Ask any legal question and get responses based on indexed case documents.")
    with st.form("question_form"):
        user_question = st.text_area("🔍 Enter your legal question:", height=100)
        show_context = st.checkbox("Show retrieved context", value=False)
        submitted = st.form_submit_button("Get Answer")
    if submitted:
        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving and generating answer..."):
                try:
                    inputs = augment_question(user_question)
                    answer = generate_answer(inputs)
                    st.markdown("### 🧠 Answer:")
                    st.success(answer)
                    if show_context:
                        st.markdown("### 📄 Retrieved Context:")
                        st.code(inputs['context'][:3000], language="markdown")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
