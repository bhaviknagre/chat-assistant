from retriever import retrieve_legal_documents
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


prompt = PromptTemplate(
    template="""
    You are a helpful legal assistant.
    Answer ONLY from the provided legal document context.
    If the context is insufficient, say you don't know.

    Context:
    {context}

    Question: {question}
    """,
    input_variables=["context", "question"]
)

def generate_answer(question: str, k: int = 5) -> str:
   
    retrieved_docs = retrieve_legal_documents(question)
    
    if not retrieved_docs:
        return "No relevant documents found."

    
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

  
    final_prompt = prompt.format(context=context_text, question=question)


    response = llm.invoke(final_prompt)

    return response.content
