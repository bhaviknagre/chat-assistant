from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


prompt = PromptTemplate(
    template="""
            You are a highly intelligent legal assistant designed to help lawyers and legal professionals by answering factual, procedural, and legal questions accurately.

            Use the following rules when responding:

            1. Use only the information present in the provided context.
            2. If the answer is not available in the context, respond exactly with:
            → "Answer is not available in the content."
            3. Your response must be:
            - Factually accurate
            - Legally sound
            - Complete and unambiguous
            4. Use professional, jurisdiction-neutral legal language.
            5. Support your answer with names, dates, cities, or case details if available in the context.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """,
    input_variables=["context", "question"]
)

def generate_answer(inputs: dict) -> str:
    """
    Expects a dict with 'context' and 'question'
    Returns formatted LLM response as string.
    """
    context = inputs.get("context", "").strip()
    question = inputs.get("question", "").strip()

    if not context:
        return "Answer is not available in the content."

    final_prompt = prompt.format(context=context, question=question)
    response = llm.invoke(final_prompt)
    return response.content
