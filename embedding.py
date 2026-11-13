
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):

    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":

    sample_chunks = [
        "Python is a programming language.",
        "Python is used in machine learning.",
        "Java is an object-oriented language."
    ]

    embeddings = create_embeddings(sample_chunks)

    print("Total embeddings:", len(embeddings))

    print("Embedding dimensions:", embeddings.shape)

    print("\nFirst embedding:")
    print(embeddings[0])
