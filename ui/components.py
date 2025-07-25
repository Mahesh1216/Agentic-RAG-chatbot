import streamlit as st

def file_uploader_component():
    """
    Streamlit component for uploading files.
    """
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "pptx", "docx", "csv", "txt", "md"])
    return uploaded_file

def chat_input_component():
    """
    Streamlit component for chat input.
    """
    user_query = st.chat_input("Ask a question about the document...")
    return user_query

def message_display_component(role: str, content: str):
    """
    Streamlit component for displaying chat messages.
    """
    with st.chat_message(role):
        st.markdown(content)

def clear_chat_button():
    """
    Streamlit component for a clear chat button.
    """
    if st.button("Clear Chat"): # Reason: Provides a way to reset the chat history.
        st.session_state.messages = []
        st.rerun()