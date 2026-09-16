import time
import streamlit as st

from rag.utils.helper import get_pdf_files
from rag.graph import graph
from rag.memory import memory
from rag.upload_pdf import upload_pdf
from rag.delete_pdf import delete_pdf
from rag.download_chat import ChatDownloader
from streamlit_mic_recorder import mic_recorder

from rag.speech import SpeechToText


# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Research Assistant")


# ------------------------------------------------
# Typing Animation
# ------------------------------------------------

def stream_text(text):

    words = text.split()

    for word in words:

        yield word + " "

        time.sleep(0.02)


# ------------------------------------------------
# Session State
# ------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------------------
# Sidebar
# ------------------------------------------------

st.sidebar.header("⚙ Settings")


# ======================================================
# Upload PDF
# ======================================================

st.sidebar.subheader("📤 Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.sidebar.button("Upload"):

        progress_bar = st.sidebar.progress(0)

        status = st.sidebar.empty()

        success, message = upload_pdf(
            uploaded_file,
            progress_bar,
            status
        )

        if success:

            st.sidebar.success(message)

            st.sidebar.info("Refreshing document list...")

            st.rerun()

        else:

            st.sidebar.error(message)


# ======================================================
# Delete PDF
# ======================================================

st.sidebar.subheader("🗑 Delete PDF")

pdf_files = get_pdf_files()

if pdf_files:

    delete_pdf_name = st.sidebar.selectbox(
        "Select PDF to Delete",
        pdf_files,
        key="delete_pdf"
    )

    if st.sidebar.button("Delete PDF"):

        success, message = delete_pdf(delete_pdf_name)

        if success:

            st.sidebar.success(message)

            st.sidebar.info("Refreshing document list...")

            st.rerun()

        else:

            st.sidebar.error(message)

else:

    st.sidebar.info("No PDFs available.")


# ======================================================
# PDF Selection
# ======================================================

pdf_files = get_pdf_files()

selected_pdf = st.sidebar.selectbox(
    "📄 Select Document",
    ["All Documents"] + pdf_files
)


# ======================================================
# Clear Conversation
# ======================================================

if st.sidebar.button("🗑 Clear Conversation"):

    st.session_state.messages = []

    memory.clear()

    st.sidebar.success("Conversation Cleared")

    st.rerun()


# ------------------------------------------------
# Display Previous Messages
# ------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ------------------------------------------------
# Voice Input
# ------------------------------------------------

st.sidebar.subheader("🎤 Voice Input")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="voice"
)

voice_question = None

if audio:

    print("\n===== AUDIO RECEIVED =====")
    print(audio)

    with st.sidebar.spinner("🎤 Converting speech to text..."):
        success, result = SpeechToText.convert(audio)

    print("Speech Success:", success)
    print("Speech Result:", result)

    if success:

        st.sidebar.success("Speech Recognized")
        st.sidebar.write(result)

        voice_question = result

        print("Voice Question:", voice_question)

    else:

        st.sidebar.error(result)


# ------------------------------------------------
# Chat Input
# ------------------------------------------------

typed_question = st.chat_input(
    "Ask a Question..."
)

question = typed_question

if voice_question:

    question = voice_question

if question:

    # --------------------------------------------
    # Save User Message
    # --------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------------
    # AI Typing Indicator
    # --------------------------------------------

    typing_status = st.empty()

    typing_status.info("🤖 AI is typing...")

    with st.spinner("Thinking..."):

        result = graph.invoke(
            {
                "question": question,
                "document_name": (
                    None
                    if selected_pdf == "All Documents"
                    else selected_pdf
                )
            }
        )
    typing_status.empty()

    decision = result.get("decision", "")

    answer = result.get("answer", "")

    documents = result.get("documents", [])

    web_results = result.get("web_results", "")

    # --------------------------------------------
    # Assistant Response
    # --------------------------------------------

    with st.chat_message("assistant"):

        if decision:

            st.info(f"🧠 Tool Selected: **{decision}**")

        # ============================================
        # ChatGPT Streaming Animation
        # ============================================

        st.write_stream(stream_text(answer))

        # ----------------------------------------
        # Citation Scoring
        # ----------------------------------------

        if documents:

            st.markdown("## ⭐ Citation Scoring")

            for index, doc in enumerate(documents, start=1):

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                page = doc.metadata.get(
                    "page",
                    "?"
                )

                similarity = doc.metadata.get(
                    "similarity",
                    0
                )

                with st.expander(
                    f"📄 Source {index}"
                ):

                    st.markdown(
                        f"**Document:** {source}"
                    )

                    st.markdown(
                        f"**Page:** {page}"
                    )

                    st.markdown(
                        f"**Similarity:** {similarity}%"
                    )

                    st.progress(
                        similarity / 100
                    )

                    st.divider()

                    st.write(
                        doc.page_content
                    )

        # ----------------------------------------
        # Web Search Results
        # ----------------------------------------

        if web_results:

            st.markdown("## 🌐 Web Search Results")

            st.markdown(web_results)

    # --------------------------------------------
    # Save Assistant Message
    # --------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # ======================================================
# Download Chat
# ======================================================

st.sidebar.subheader("📥 Download Chat")

if st.session_state.messages:

    txt_data = ChatDownloader.create_txt(
        st.session_state.messages
    )

    st.sidebar.download_button(
        "📄 Download TXT",
        data=txt_data,
        file_name="chat.txt",
        mime="text/plain"
    )

    docx_data = ChatDownloader.create_docx(
        st.session_state.messages
    )

    st.sidebar.download_button(
        "📝 Download DOCX",
        data=docx_data,
        file_name="chat.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    pdf_data = ChatDownloader.create_pdf(
        st.session_state.messages
    )

    st.sidebar.download_button(
        "📕 Download PDF",
        data=pdf_data,
        file_name="chat.pdf",
        mime="application/pdf"
    )

else:

    st.sidebar.info(
        "No conversation available."
    )