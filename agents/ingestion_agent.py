import logging
import os
from agents.base_agent import BaseAgent
from mcp.message_types import MessageType, MCPMessage
from processors.pdf_processor import PDFProcessor
from processors.pptx_processor import PPTXProcessor
from processors.docx_processor import DOCXProcessor
from processors.csv_processor import CSVProcessor
from processors.text_processor import TextProcessor
from vector_store.faiss_store import FAISSVectorStore
from utils.helpers import get_file_extension

logger = logging.getLogger(__name__)

class IngestionAgent(BaseAgent):
    """
    The IngestionAgent is responsible for processing documents, extracting text,
    chunking it, generating embeddings, and adding them to the vector store.
    """
    def __init__(self, message_bus):
        super().__init__("IngestionAgent", message_bus)
        self.vector_store = FAISSVectorStore()
        self.processors = {
            ".pdf": PDFProcessor(),
            ".pptx": PPTXProcessor(),
            ".docx": DOCXProcessor(),
            ".csv": CSVProcessor(),
            ".txt": TextProcessor(),
            ".md": TextProcessor(),
        }
        logger.info("IngestionAgent initialized.")

    async def setup(self):
        """Sets up the agent, including registering message handlers."""
        await self.register_handler(MessageType.INGESTION_REQUEST, self.handle_ingestion_request)
        logger.info("IngestionAgent setup complete and handler for INGESTION_REQUEST registered.")

    async def run(self):
        """Runs the agent's main logic. For IngestionAgent, this is a no-op as it's event-driven."""
        pass

    async def handle_ingestion_request(self, message: MCPMessage):
        """
        Handles an ingestion request by processing the document and adding it to the vector store.
        """
        file_path = message.payload.file_path
        request_id = message.payload.request_id
        logger.info(f"IngestionAgent received request for file: {file_path} (Request ID: {request_id})")

        if not os.path.exists(file_path):
            logger.error(f"File not found for ingestion: {file_path}")
            await self.send_message(
                MessageType.INGESTION_RESPONSE,
                {
                    "request_id": request_id,
                    "status": "failed",
                    "message": f"File not found: {file_path}"
                }
            )
            return

        file_extension = get_file_extension(file_path)
        processor = self.processors.get(file_extension)

        if not processor:
            logger.error(f"No processor found for file type: {file_extension}")
            await self.send_message(
                MessageType.INGESTION_RESPONSE,
                {
                    "request_id": request_id,
                    "status": "failed",
                    "message": f"Unsupported file type: {file_extension}"
                }
            )
            return

        try:
            chunks = processor.process(file_path)
            if chunks:
                self.vector_store.add_documents(chunks)
                logger.info(f"Successfully ingested and added {len(chunks)} chunks from {file_path} to vector store.")
                await self.send_message(
                    MessageType.INGESTION_RESPONSE,
                    {
                        "request_id": request_id,
                        "status": "success",
                        "message": f"Successfully ingested {len(chunks)} chunks from {file_path}"
                    }
                )
            else:
                logger.warning(f"No chunks extracted from {file_path}.")
                await self.send_message(
                    MessageType.INGESTION_RESPONSE,
                    {
                        "request_id": request_id,
                        "status": "failed",
                        "message": f"No content extracted or chunks generated from {file_path}"
                    }
                )
        except Exception as e:
            logger.error(f"Error during ingestion of {file_path}: {e}")
            await self.send_message(
                MessageType.INGESTION_RESPONSE,
                {
                    "request_id": request_id,
                    "status": "failed",
                    "message": f"Error during ingestion: {str(e)}"
                }
            )