import streamlit as st
import os
from utils.pipeline import run_pipeline
from utils.document_loader import load_document
from utils.chunks import split_loaded_document

# Configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="📄 LawAI: Document Indexer", layout="wide")
st.title("📚 LawAI: Document Indexer + Embedder with Chroma")
st.markdown("Upload a document to extract text, split into chunks, generate embeddings, and store with ChromaDB.")

# File Upload
uploaded_file = st.file_uploader("Upload a document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

file_path = None
if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File uploaded and saved to `{file_path}`")

# Run pipeline only when button is clicked
if file_path and st.button("🚀 Run Pipeline"):
    with st.spinner("Running full pipeline (load → chunk → embed → store)..."):
        try:
            run_pipeline(file_path)
            st.success("🎉 Document processed and stored successfully in ChromaDB!")

            # Optional Preview After Processing
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
