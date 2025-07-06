# app.py
import streamlit as st
from rag_pipeline.augmentation import augment_question
from rag_pipeline.generation import generate_answer

st.set_page_config(page_title="Legal RAG Assistant", layout="wide")

st.title("📚 Legal AI Assistant")
st.markdown("Ask any legal question and get responses based on indexed case documents.")

# Input form
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
                # 1. Augment with context
                inputs = augment_question(user_question)

                # 2. Generate answer
                answer = generate_answer(inputs)

                # Display
                st.markdown("### 🧠 Answer:")
                st.success(answer)

                if show_context:
                    st.markdown("### 📄 Retrieved Context:")
                    st.code(inputs['context'][:3000], language="markdown")  # limit large context

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
