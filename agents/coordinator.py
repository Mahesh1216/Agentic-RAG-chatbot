import asyncio
from typing import Dict, Any
from agents.base_agent import BaseAgent
from mcp.message_types import MCPMessage, MessageType, IngestionRequestPayload, RetrievalRequestPayload, LLMRequestPayload, LLMResponsePayload, ErrorPayload
from mcp.protocol import ModelContextProtocol
from utils.logging_config import logger
from utils.helpers import generate_unique_id

class Coordinator(BaseAgent):
    """The Coordinator Agent manages the overall flow of the RAG chatbot."""

    def __init__(self, message_bus: ModelContextProtocol):
        super().__init__("CoordinatorAgent", message_bus)
        self.active_requests: Dict[str, asyncio.Queue] = {}

    async def setup(self):
        """Registers handlers for messages relevant to the Coordinator."""
        await self.register_handler(MessageType.INGESTION_COMPLETE, self._handle_ingestion_complete)
        await self.register_handler(MessageType.RETRIEVAL_RESULT, self._handle_retrieval_result)
        await self.register_handler(MessageType.LLM_RESPONSE, self._handle_llm_response)
        await self.register_handler(MessageType.ERROR, self._handle_error_message)
        logger.info("CoordinatorAgent setup complete.")

    async def run(self):
        """The Coordinator agent runs indefinitely, waiting for external requests or internal messages."""
        logger.info("CoordinatorAgent is running...")
        # In a real application, this might listen for external API calls or UI events
        while True:
            await asyncio.sleep(1) # Keep the agent alive

    async def process_query(self, query: str, file_path: str = None, file_type: str = None) -> Dict[str, Any]:
        """Initiates a new RAG process based on user query and optional file upload."""
        trace_id = generate_unique_id(query + str(file_path) + str(file_type))
        response_queue = asyncio.Queue(1)
        self.active_requests[trace_id] = response_queue

        if file_path and file_type:
            logger.info(f"Coordinator: Initiating ingestion for {file_path} (Trace ID: {trace_id})")
            ingestion_payload = IngestionRequestPayload(file_path=file_path, file_type=file_type, document_id=trace_id)
            await self.send_message(
                MCPMessage(
                    sender=self.agent_id,
                    receiver="IngestionAgent",
                    type=MessageType.INGESTION_REQUEST,
                    trace_id=trace_id,
                    timestamp="", # Will be filled by message bus
                    payload=ingestion_payload.model_dump()
                )
            )
        else:
            logger.info(f"Coordinator: Initiating retrieval for query '{query}' (Trace ID: {trace_id})")
            retrieval_payload = RetrievalRequestPayload(query=query)
            await self.send_message(
                MCPMessage(
                    sender=self.agent_id,
                    receiver="RetrievalAgent",
                    type=MessageType.RETRIEVAL_REQUEST,
                    trace_id=trace_id,
                    timestamp="", # Will be filled by message bus
                    payload=retrieval_payload.model_dump()
                )
            )

        # Wait for the final response
        final_response = await response_queue.get()
        del self.active_requests[trace_id]
        return final_response

    async def _handle_ingestion_complete(self, message: MCPMessage):
        """Handles INGESTION_COMPLETE messages and triggers retrieval."""
        payload = IngestionRequestPayload(**message.payload) # Re-use payload for document_id
        logger.info(f"Coordinator: Ingestion complete for document {payload.document_id} (Trace ID: {message.trace_id})")

        # Assuming the original query is stored in the trace_id context or passed along
        # For simplicity, we'll assume the query is part of the initial request and needs to be retrieved
        # In a more complex system, the Coordinator would maintain state for each trace_id
        original_query = "" # Placeholder: need to retrieve original query associated with trace_id

        retrieval_payload = RetrievalRequestPayload(query=original_query, document_ids=[payload.document_id])
        await self.send_message(
            MCPMessage(
                sender=self.agent_id,
                receiver="RetrievalAgent",
                type=MessageType.RETRIEVAL_REQUEST,
                trace_id=message.trace_id,
                timestamp="",
                payload=retrieval_payload.model_dump()
            )
        )

    async def _handle_retrieval_result(self, message: MCPMessage):
        """Handles RETRIEVAL_RESULT messages and triggers LLM response generation."""
        payload = RetrievalRequestPayload(**message.payload) # Re-use payload for query
        retrieval_result = message.payload # Assuming payload directly contains top_chunks and metadata
        logger.info(f"Coordinator: Retrieval complete for query '{payload.query}' (Trace ID: {message.trace_id})")

        llm_payload = LLMRequestPayload(
            query=payload.query,
            context=retrieval_result.get("top_chunks", []),
            chat_history=[] # Placeholder for actual chat history
        )
        await self.send_message(
            MCPMessage(
                sender=self.agent_id,
                receiver="LLMAgent",
                type=MessageType.LLM_REQUEST,
                trace_id=message.trace_id,
                timestamp="",
                payload=llm_payload.model_dump()
            )
        )

    async def _handle_llm_response(self, message: MCPMessage):
        """Handles LLM_RESPONSE messages and sends the final response back to the caller."""
        payload = LLMResponsePayload(**message.payload)
        logger.info(f"Coordinator: LLM response received (Trace ID: {message.trace_id})")
        if message.trace_id in self.active_requests:
            await self.active_requests[message.trace_id].put({
                "response": payload.response,
                "source_documents": payload.source_documents
            })

    async def _handle_error_message(self, message: MCPMessage):
        """Handles ERROR messages and propagates them to the caller."""
        payload = ErrorPayload(**message.payload)
        logger.error(f"Coordinator received error from {message.sender}: {payload.message} (Trace ID: {message.trace_id})")
        if message.trace_id in self.active_requests:
            await self.active_requests[message.trace_id].put({
                "error": payload.message,
                "details": payload.details,
                "code": payload.code
            })