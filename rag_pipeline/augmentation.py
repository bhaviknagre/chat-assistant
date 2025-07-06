from rag_pipeline.retriever import retrieve_legal_documents

def augment_question(question: str, k: int = 5) -> dict:
    """
    Retrieve relevant context for the given legal question.
    Returns a dict with keys: 'context', 'question'
    """
    retrieved_docs = retrieve_legal_documents(question)
    
    if not retrieved_docs:
        return {
            "context": "No relevant documents found.",
            "question": question
        }

    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    return {
        "context": context_text,
        "question": question
    }

