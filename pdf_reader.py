
from pypdf import PdfReader

def load_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


if __name__ == "__main__":

    extracted_text = load_pdf("sample.pdf")

    print(extracted_text)
