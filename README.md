
# Legal RAG Assistant — Full Project Documentation

---

## 1. Project Overview

**Legal RAG Assistant**  is a Retrieval-Augmented Generation (RAG) system designed for legal professionals. It allows:

- Uploading documents and images (PDF, DOCX, TXT, PNG, JPG)

- Extracting content and embedding via OpenAI

- Storing in a vector DB (Chroma)

- Asking legal questions through a chatbot UI (Streamlit)

- Getting answers based only on uploaded documents 

---

## 2. System Architecture

### 2.1 High-Level Diagram

```
User
 │
 │ 1. Uploads Document / Asks Question
 │
 ▼
[Streamlit UI]
 │
 ├──▶ [Document Loader] ──▶ [Chunker] ──▶ [Embedding Generator] ──▶ [Chroma Vector Store]
 │                                 │
 │                                 ▼
 └────────────────────────────────▶ [Retriever] ◀── [LLM (OpenAI)]
                                      │
                                      ▼
                                 [Answer Generator]
                                      │
                                      ▼
                                   [UI Output]
```

### 2.2 Workflow

#### Document Indexing
1. **Upload**: User uploads a document via Streamlit UI (`app.py`).
2. **Load**: Text is extracted from the document (`utils/document_loader.py`).
3. **Chunk**: Text is split into overlapping chunks (`utils/chunks.py`).
4. **Embed**: Each chunk is embedded using OpenAI (`utils/embedding_generator.py`).
5. **Store**: Embeddings and metadata are stored in ChromaDB (`utils/store_house.py`).

#### Question Answering
1. **Ask**: User submits a question via chat UI (`chat_app.py`).
2. **Retrieve**: Relevant chunks are retrieved from ChromaDB (`rag_pipeline/retriever.py`, `rag_pipeline/augmentation.py`).
3. **Generate**: LLM generates an answer using only the retrieved context (`rag_pipeline/generation.py`).
4. **Display**: Answer (and optionally, context) is shown in the UI.

---

## 3. Module & File Breakdown

### 3.1 Streamlit Apps
- **`app.py`**: UI for document upload and indexing. Runs the full pipeline and previews results.
- **`chat_app.py`**: UI for chat-based Q&A. Handles question input, context retrieval, and answer display.

### 3.2 RAG Pipeline (`rag_pipeline/`)
- **`augmentation.py`**: Retrieves relevant context for a question using the retriever.
- **`generation.py`**: Formats the prompt and invokes the LLM to generate an answer.
- **`retriever.py`**: Sets up the Chroma vector store and multi-query retriever using OpenAI embeddings.
- **`rag_pipeline.py`**: (Optional) Example of a full pipeline for retrieval and answer generation.

### 3.3 Utilities (`utils/`)
- **`document_loader.py`**: Loads and parses PDF, DOCX, and TXT files into LangChain Document objects.
- **`chunks.py`**: Splits documents into overlapping text chunks using token-aware splitting.
- **`embedding_generator.py`**: Generates vector embeddings for text chunks using OpenAI's API.
- **`store_house.py`**: Stores embeddings and metadata in a persistent ChromaDB collection.
- **`pipeline.py`**: Orchestrates the full document indexing pipeline (load → chunk → embed → store).
- **`logger.py`**: Configures logging for all major operations and errors.

### 3.4 Data & Storage
- **`uploads/`**: Stores uploaded documents.
- **`chroma_store/`**: Persistent ChromaDB vector store.
- **`logs/`**: Log files for debugging and monitoring.

---

## 3.5 Demo

![Image](screenshots/interface.png)



## 4. Setup & Configuration

### 4.1 Prerequisites
- Python 3.10+
- OpenAI API key

### 4.2 Installation
1. **Clone the repository**
2. **Create a virtual environment**
   ```sh
   python -m venv myenv
   myenv\Scripts\activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file in the root directory:
     ```env
     OPENAI_API_KEY="sk-..."
     ```

### 4.3 Directory Structure
```
├── app.py
├── chat_app.py
├── rag_pipeline/
│   ├── augmentation.py
│   ├── generation.py
│   ├── retriever.py
├── utils/
│   ├── document_loader.py
│   ├── chunks.py
│   ├── embedding_generator.py
│   ├── store_house.py
│   ├── pipeline.py
│   ├── photo_ocr.py      <
│   └── logger.py
├── uploads/
├── chroma_store/
├── logs/
├── screenshots/          
├── requirements.txt
├── .env
└── DOCUMENTATION.md

```

---

## 5. Usage Guide

### 5.1 Indexing Documents
1. Run the indexer app:
   ```sh
   streamlit run app.py
   ```
2. Upload a `.pdf`, `.docx`, or `.txt` file.
3. Click "Run Pipeline" to process and store the document.
4. Preview extracted text and chunks in the UI.

### 5.2 Asking Questions
1. Run the chat app:
   ```sh
   streamlit run chat_app.py
   ```
2. Enter your legal question.
3. (Optional) Check "Show retrieved context" to see supporting text.
4. Click "Get Answer" to receive a response based only on indexed documents.

---

## 6. Extending & Customizing

- **Add new file types**: Extend `utils/document_loader.py` to support more formats.
- **Change embedding model**: Modify `utils/embedding_generator.py` to use a different embedding provider.
- **Swap LLM**: Update `rag_pipeline/generation.py` to use another LLM (e.g., local models).
- **Tune chunking**: Adjust chunk size/overlap in `utils/chunks.py` for different document types.
- **Change vector store**: Replace ChromaDB logic in `utils/store_house.py` if needed.

---

## 7. Troubleshooting & FAQ

### Common Issues
- **Embedding errors**: Ensure your `openai` package is up-to-date and your API key is valid.
- **ChromaDB issues**: The `chroma_store/` directory must be writable.
- **Document not found**: Only `.pdf`, `.docx`, and `.txt` files are supported.
- **Environment variables**: Make sure `.env` is present and correct.

### FAQ
- **Q: Can I use other LLMs or embedding models?**
  - Yes, the code is modular. Swap out the relevant utility files.
- **Q: Is my data private?**
  - All processing is local except for OpenAI API calls.
- **Q: How do I clear the database?**
  - Delete the `chroma_store/` directory to reset the vector store.

---

## 8. Example Flows

### Example 1: Indexing a PDF
- Upload `uploads/2.pdf` via the UI.
- Pipeline logs:
  - Document loaded: 43 pages
  - Chunked: 81 chunks
  - Embeddings generated
  - Stored in ChromaDB

### Example 2: Asking a Legal Question
- Enter: "What was the final judgement in case 2160_2024_16_1502_59234?"
- System retrieves relevant chunks and generates an answer using only indexed content.

---

## 9. Logging & Monitoring
- All major steps and errors are logged to `logs/app.log`.
- Check logs for debugging failed pipelines or API issues.

---

## 10. License & Credits
- MIT License
- Built with LangChain, ChromaDB, OpenAI, and Streamlit.

---

## 11. Authors & Contact
- Your Name Here
- [Your Email/Contact]

---

## 12. References
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Streamlit Docs](https://docs.streamlit.io/)
=======

## Detailed Description of Core Components


**Document Extraction (file_extraction.py) :**
This module handles the extraction of text from various document formats (e.g., PDF, DOCX). It ensures the content is extracted in a readable format for further processing.

**Text Preprocessing (preprocess.py) :**
Text extracted from documents often contains unwanted characters, noise, and formatting issues. This module cleans the text and prepares it for chunking and embedding.

**Chunking (chunks.py) :**
After preprocessing, the text is divided into smaller segments (chunks). This is essential for embedding and storing in a FAISS index.

**Embedding (embedding.py) :**
This module converts text chunks into embeddings (vector representations) using OpenAI’s embedding API. These embeddings are stored in a FAISS index for fast retrieval during semantic searches.

**Storage (storhouse.py) :**
Handles the storage of documents, metadata, embeddings, and chunked text in the SQLite database and FAISS index. It ensures that the document metadata, text, and embeddings are correctly stored and easily accessible.

**Pipeline (pipeline.py) :**
This is the orchestrator, managing the entire flow of the application from document extraction to embedding and storage. It ensures that the process is executed in a streamlined manner.

>>>>>>> 78da8544f2b9893ad8480257c3fe3d8c56a6bc7b
