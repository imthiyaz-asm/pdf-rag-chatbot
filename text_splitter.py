
def split_text(text, chunk_size=500, overlap=50):

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size")

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":

    from pdf_reader import load_pdf

    extracted_text = load_pdf("sample.pdf")

    chunks = split_text(extracted_text)

    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks):

        print(f"\n--- Chunk {index + 1} ---")

        print(chunk)
