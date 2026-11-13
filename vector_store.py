
import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or access the collection
collection = client.get_or_create_collection(
    name="pdf_documents"
)


# Store PDF chunks in ChromaDB
def store_chunks(chunks):

    if not chunks:
        raise ValueError("No text chunks found in the PDF.")

    # Delete previously stored chunks
    existing_data = collection.get()

    if existing_data["ids"]:
        collection.delete(ids=existing_data["ids"])

    # Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # Store new chunks
    collection.upsert(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print("Chunks stored successfully!")
    print("Total stored chunks:", collection.count())


# Search for relevant PDF chunks
def search(question, k=3):

    total_chunks = collection.count()

    if total_chunks == 0:
        return {"documents": [[]]}

    # Convert question into embedding
    question_embedding = model.encode([question]).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(k, total_chunks)
    )

    return results


# Execute only when running this file directly
if __name__ == "__main__":

    from pdf_reader import load_pdf
    from text_splitter import split_text

    # Read sample PDF
    text = load_pdf("sample.pdf")

    # Split extracted text
    chunks = split_text(text)

    # Store chunks
    store_chunks(chunks)

    print("PDF processing completed!")
