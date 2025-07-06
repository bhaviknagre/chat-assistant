from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

chroma_store = Chroma(
    collection_name="legal_documents",
    embedding_function=embedding_model,
    persist_directory="chroma_store"
)

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)


multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=chroma_store.as_retriever(search_kwargs={"k": 10}),
    llm=llm
)

def retrieve_legal_documents(query: str):
    return multi_query_retriever.get_relevant_documents(query)
