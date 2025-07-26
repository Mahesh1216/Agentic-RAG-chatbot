import logging
import traceback
from agents.base_agent import BaseAgent
from mcp.message_types import MessageType, MCPMessage, LLMRequestPayload, LLMResponsePayload, ErrorPayload
from config.settings import settings
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class LLMAgent(BaseAgent):
    """
    The LLMAgent is responsible for interacting with the Language Model to generate responses.
    """
    def __init__(self, message_bus):
        super().__init__("LLMAgent", message_bus)
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model_name = settings.LLM_MODEL_NAME
        self.temperature = settings.LLM_TEMPERATURE
        self.client = genai.GenerativeModel(self.model_name)
        logger.info("LLMAgent initialized.")
        
    async def setup(self):
        """Sets up the agent, including registering message handlers."""
        await self.register_handler(MessageType.LLM_REQUEST, self.handle_llm_request)
        logger.info("LLMAgent setup complete and handler for LLM_REQUEST registered.")
        
    async def run(self):
        """Runs the agent's main logic. For LLMAgent, this is a no-op as it's event-driven."""
        pass

    async def handle_llm_request(self, message: MCPMessage):
        """
        Handles an LLM request by generating a response based on the provided prompt and context.
        """
        payload = LLMRequestPayload(**message.payload)
        logger.info(f"LLMAgent received request (Trace ID: {message.trace_id})")

        try:
            # Gemini expects a single string or a list of Content objects, not OpenAI-style {role, content} dicts
            context_str = "\n".join(payload.context)
            prompt = f"Context:\n{context_str}\n\nQuestion: {payload.query}"

            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=self.temperature
                )
            )
            llm_response_content = response.text
            logger.info(f"Successfully generated LLM response for trace ID: {message.trace_id}")

            # Prepare source_documents list from context and metadata if available
            source_documents = []
            if hasattr(payload, 'metadata') and payload.metadata:
                for idx, chunk in enumerate(payload.context):
                    meta = payload.metadata.get(str(idx), {}) if isinstance(payload.metadata, dict) else {}
                    source_documents.append({"content": chunk, "metadata": meta})
            else:
                for chunk in payload.context:
                    source_documents.append({"content": chunk, "metadata": {}})

            # Send the response back to the Coordinator
            response_payload = LLMResponsePayload(
                response=llm_response_content,
                source_documents=source_documents,
                trace_id=message.trace_id
            )
            await self.send_message(
                MCPMessage(
                    sender=self.agent_id,
                    receiver="CoordinatorAgent",
                    type=MessageType.LLM_RESPONSE,
                    trace_id=message.trace_id,
                    timestamp="",
                    payload=response_payload.model_dump()
                )
            )
        except Exception as e:
            logger.error(f"Error generating LLM response for trace ID {message.trace_id}: {e}")
            error_payload = ErrorPayload(
                code="LLM_ERROR",
                message=f"Error generating response: {str(e)}",
                details=traceback.format_exc()
            )
            await self.send_message(
                MCPMessage(
                    sender=self.agent_id,
                    receiver="CoordinatorAgent",
                    type=MessageType.ERROR,
                    trace_id=message.trace_id,
                    timestamp="",
                    payload=error_payload.model_dump()
                )
            )