
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env file")

# Connect to Groq
client = Groq(api_key=api_key)


def generate_answer(context, question):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PDF question-answering assistant. "
                    "Answer only using the provided context. "
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
