import streamlit as st
import asyncio
import logging
from ui.components import file_uploader_component, chat_input_component, message_display_component, clear_chat_button
from mcp.message_bus import InMemoryMessageBus
from agents.coordinator import Coordinator
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_agent import LLMAgent
from mcp.message_types import MessageType, MCPMessage
from utils.helpers import generate_unique_id
from config.settings import settings
import os

logger = logging.getLogger(__name__)

class ChatInterface:
    """
    Manages the Streamlit chat interface and orchestrates communication between UI and agents.
    """
    def __init__(self):
        self.message_bus = InMemoryMessageBus()
        self.coordinator = Coordinator(self.message_bus)
        self.ingestion_agent = IngestionAgent(self.message_bus)
        self.retrieval_agent = RetrievalAgent(self.message_bus)
        self.llm_agent = LLMAgent(self.message_bus)

        # Initialize session state for messages if not already present
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "file_processed" not in st.session_state:
            st.session_state.file_processed = False

        # self.setup_mcp_handlers() # Handlers will be registered in agent setup
        logger.info("ChatInterface initialized.")

    async def setup_agents(self):
        await self.ingestion_agent.setup()
        await self.retrieval_agent.setup()
        await self.llm_agent.setup()
        self.setup_mcp_handlers()
        logger.info("All agents setup complete.")

    def setup_mcp_handlers(self):
        """
        Sets up handlers for MCP messages to update the UI.
        """
        async def handle_ingestion_response(message: MCPMessage):
            if message.payload.status == "success":
                st.session_state.file_processed = True
                st.session_state.messages.append({"role": "assistant", "content": "Document processed successfully! You can now ask questions."})
            else:
                st.session_state.messages.append({"role": "assistant", "content": f"Document processing failed: {message.payload.message}"})
            st.rerun() # Trigger rerun to update UI

        async def handle_llm_response(message: MCPMessage):
            if message.payload.status == "success":
                st.session_state.messages.append({"role": "assistant", "content": message.payload.response})
            else:
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {message.payload.response}"})
            st.rerun() # Trigger rerun to update UI

        asyncio.create_task(self.message_bus.register_handler(MessageType.INGESTION_RESPONSE, handle_ingestion_response))
        asyncio.create_task(self.message_bus.register_handler(MessageType.LLM_RESPONSE, handle_llm_response))

    async def run(self):
        """
        Runs the Streamlit application interface.
        """
        st.set_page_config(page_title="Agentic RAG Chatbot", layout="centered")
        st.title("Agentic RAG Chatbot")

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            message_display_component(message["role"], message["content"])

        # File uploader
        uploaded_file = file_uploader_component()
        if uploaded_file and not st.session_state.file_processed:
            with st.spinner("Processing document..."):
                # Save the uploaded file temporarily
                os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
                file_path = os.path.join(settings.UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                request_id = generate_unique_id(uploaded_file.name)
                ingestion_payload = {
                    "request_id": request_id,
                    "file_path": file_path,
                    "file_type": os.path.splitext(uploaded_file.name)[1]
                }
                await self.coordinator.send_message(MessageType.INGESTION_REQUEST, ingestion_payload)
                st.session_state.messages.append({"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})
                st.session_state.file_processed = True # Mark as processing started
                st.rerun() # Rerun to show "processing" message

        # Chat input
        user_query = chat_input_component()
        if user_query and st.session_state.file_processed:
            st.session_state.messages.append({"role": "user", "content": user_query})
            message_display_component("user", user_query)

            request_id = generate_unique_id(user_query)
            query_payload = {
                "request_id": request_id,
                "query": user_query
            }
            await self.coordinator.send_message(MessageType.RETRIEVAL_REQUEST, query_payload)
            st.session_state.messages.append({"role": "assistant", "content": "Thinking..."})
            st.rerun() # Rerun to show "thinking" message

        clear_chat_button()

# To run the Streamlit app, save this file as e.g., `app.py` and run `streamlit run app.py`
# The main app.py will instantiate and run this class.