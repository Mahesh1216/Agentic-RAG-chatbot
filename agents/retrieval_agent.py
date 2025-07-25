import logging
from agents.base_agent import BaseAgent
from mcp.message_types import MessageType, MCPMessage
from vector_store.faiss_store import FAISSVectorStore

logger = logging.getLogger(__name__)

class RetrievalAgent(BaseAgent):
    """
    The RetrievalAgent is responsible for retrieving relevant information from the
    vector store based on a user query.
    """
    def __init__(self, message_bus):
        super().__init__("RetrievalAgent", message_bus)
        self.vector_store = FAISSVectorStore()
        logger.info("RetrievalAgent initialized.")
        
    async def setup(self):
        """Sets up the agent, including registering message handlers."""
        await self.register_handler(MessageType.RETRIEVAL_REQUEST, self.handle_retrieval_request)
        logger.info("RetrievalAgent setup complete and handler for RETRIEVAL_REQUEST registered.")
        
    async def run(self):
        """Runs the agent's main logic. For RetrievalAgent, this is a no-op as it's event-driven."""
        pass

    async def handle_retrieval_request(self, message: MCPMessage):
        """
        Handles a retrieval request by querying the vector store and returning
        the most relevant documents.
        """
        query = message.payload.query
        request_id = message.payload.request_id
        top_k = message.payload.top_k
        logger.info(f"RetrievalAgent received request for query: '{query}' (Request ID: {request_id})")

        try:
            retrieved_docs = self.vector_store.search(query, k=top_k)
            if retrieved_docs:
                logger.info(f"Successfully retrieved {len(retrieved_docs)} documents for query '{query}'.")
                await self.send_message(
                    MessageType.RETRIEVAL_RESULT,
                    {
                        "request_id": request_id,
                        "status": "success",
                        "query": query,
                        "documents": retrieved_docs
                    }
                )
            else:
                logger.warning(f"No documents found for query '{query}'.")
                await self.send_message(
                    MessageType.RETRIEVAL_RESULT,
                    {
                        "request_id": request_id,
                        "status": "failed",
                        "query": query,
                        "documents": [],
                        "message": "No relevant documents found."
                    }
                )
        except Exception as e:
            logger.error(f"Error during retrieval for query '{query}': {e}")
            await self.send_message(
                MessageType.RETRIEVAL_RESULT,
                {
                    "request_id": request_id,
                    "status": "failed",
                    "query": query,
                    "documents": [],
                    "message": f"Error during retrieval: {str(e)}"
                }
            )