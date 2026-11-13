
from vector_store import search
from llm import generate_answer


def chat_with_pdf(question):

    # Retrieve relevant chunks
    results = search(question, k=3)

    retrieved_chunks = results["documents"][0]

    if not retrieved_chunks:
        return "I don't know based on the provided PDF."

    # Combine retrieved chunks
    context = "\n\n".join(retrieved_chunks)

    # Generate answer using Groq
    answer = generate_answer(context, question)

    return answer


if __name__ == "__main__":

    print("Welcome to PDF RAG Chatbot!")

    while True:

        question = input("\nAsk a question about your PDF (type exit to quit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = chat_with_pdf(question)

        print("\nAnswer:")
        print(answer)
