
import streamlit as st
import hashlib
from io import BytesIO
from pypdf import PdfReader

from text_splitter import split_text
from vector_store import store_chunks, search
from llm import generate_answer


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DocuMind | AI PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263247;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(120deg, #172554, #312e81, #1e1b4b);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #3730a3;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ffffff;
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #c7d2fe;
    font-size: 15px;
    margin-bottom: 0;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #f9fafb;
    margin-top: 20px;
    margin-bottom: 15px;
}

.info-card {
    background: #151f32;
    border: 1px solid #293750;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}

.info-card h4 {
    color: #c4b5fd;
    margin-bottom: 8px;
}

.info-card p {
    color: #aebbd0;
    font-size: 14px;
    margin-bottom: 0;
}

div[data-testid="stChatMessage"] {
    background: #151f32;
    border: 1px solid #293750;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 12px;
}

.stChatInput textarea {
    background: #151f32 !important;
    color: white !important;
}

.stButton button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover {
    border: 1px solid #a78bfa;
    color: white;
}

.stFileUploader {
    background: #151f32;
    border: 1px dashed #6366f1;
    border-radius: 12px;
    padding: 10px;
}

hr {
    border-color: #293750;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_file_hash" not in st.session_state:
    st.session_state.processed_file_hash = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "processing_error" not in st.session_state:
    st.session_state.processing_error = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 📚 DocuMind")

    st.caption("YOUR PERSONAL AI DOCUMENT ASSISTANT")

    st.divider()

    st.markdown("### 📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose your PDF",
        type=["pdf"],
        help="Upload a text-based PDF document."
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        if file_hash != st.session_state.processed_file_hash:

            with st.spinner("Reading and processing PDF..."):

                try:

                    reader = PdfReader(BytesIO(file_bytes))

                    text = ""

                    for page in reader.pages:
                        text += (page.extract_text() or "") + "\n"

                    if not text.strip():
                        raise ValueError(
                            "No readable text found in this PDF."
                        )

                    chunks = split_text(text)

                    store_chunks(chunks)

                    st.session_state.processed_file_hash = file_hash
                    st.session_state.pdf_name = uploaded_file.name
                    st.session_state.messages = []
                    st.session_state.processing_error = None

                except Exception as error:

                    st.session_state.processing_error = str(error)

                    st.session_state.processed_file_hash = None
                    st.session_state.pdf_name = None

        if st.session_state.processing_error:

            st.error(
                f"PDF processing failed: "
                f"{st.session_state.processing_error}"
            )

        elif st.session_state.processed_file_hash == file_hash:

            st.success("✓ Document processed successfully")

    st.divider()

    st.markdown("### 📌 Current Document")

    if st.session_state.pdf_name:

        st.markdown(
            f"""
            <div class="info-card">
                <h4>📄 Document Ready</h4>
                <p>{st.session_state.pdf_name}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("Upload a PDF to begin chatting.")

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Python • ChromaDB • Groq")


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown(
    """
    <div class="hero">
        <h1>Chat with Your Documents </h1>
        <p>
            Upload a PDF, ask questions, and get intelligent
            answers grounded in your document.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# INFORMATION CARDS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h4>📄 Document Upload</h4>
            <p>Upload and process your PDF documents.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h4>🔍 Smart Search</h4>
            <p>Find relevant information using semantic search.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <h4>🤖 AI Answers</h4>
            <p>Get answers generated using your document context.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# CHAT SECTION
# ==========================================

st.markdown(
    '<div class="section-title">💬 Conversation</div>',
    unsafe_allow_html=True
)


# Display previous conversation

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT AND RESPONSE
# ==========================================

question = st.chat_input(
    "Ask anything about your uploaded PDF..."
)


if question:

    if st.session_state.processed_file_hash is None:

        st.warning("Please upload a PDF before asking questions.")

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing your document..."):

                try:

                    # Retrieve relevant chunks
                    results = search(question, k=3)

                    retrieved_chunks = results["documents"][0]

                    if not retrieved_chunks:

                        answer = (
                            "I don't know based on the provided PDF."
                        )

                    else:

                        # Combine retrieved chunks
                        context = "\n\n".join(retrieved_chunks)

                        # Generate answer
                        answer = generate_answer(
                            context,
                            question
                        )

                    st.markdown(answer)

                    # Display sources
                    if retrieved_chunks:

                        with st.expander("🔍 View retrieved PDF content"):

                            for index, chunk in enumerate(
                                retrieved_chunks,
                                start=1
                            ):

                                st.markdown(f"**Source {index}**")
                                st.write(chunk)
                                st.divider()

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as error:

                    st.error(f"Error generating answer: {error}")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#8492a6; padding:15px;">
        Built using Python, Streamlit, ChromaDB and Groq
        <br>
        <small>DocuMind - AI Powered PDF Assistant</small>
    </div>
    """,
    unsafe_allow_html=True
)
