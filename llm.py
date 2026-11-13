
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# ==================================
# LOAD API KEY
# ==================================

# Load local .env file
load_dotenv()

# First check Streamlit Cloud Secrets
# If unavailable, use local .env
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")


# Validate API key
if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Configure it in your .env file or Streamlit Secrets."
    )


# ==================================
# CONNECT TO GROQ
# ==================================

client = Groq(api_key=api_key)


# ==================================
# GENERATE AI ANSWER
# ==================================

def generate_answer(context, question):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PDF question-answering assistant. "
                    "Answer only using the provided context. "
                    "Do not use outside knowledge. "
                    "If the answer is not present in the context, "
                    "say: I don't know based on the provided PDF."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content
