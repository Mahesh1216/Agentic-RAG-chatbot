import logging
from agents.base_agent import BaseAgent
from mcp.message_types import MessageType, MCPMessage
from config.settings import settings
import google.generativeai as genai
import os

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
        prompt = message.payload.prompt
        context = message.payload.context
        request_id = message.payload.request_id
        logger.info(f"LLMAgent received request (Request ID: {request_id})")

        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
            ]
            
            response = await self.client.generate_content_async(
                contents=messages,
                generation_config=genai.GenerationConfig(
                    temperature=self.temperature
                )
            )
            llm_response_content = response.text
            logger.info(f"Successfully generated LLM response for request ID: {request_id}")
            await self.send_message(
                 MessageType.LLM_RESPONSE,
                 {
                     "request_id": request_id,
                     "status": "success",
                     "response": llm_response_content,
                     "source_documents": [],
                     "trace_id": message.trace_id
                 }
             )
        except Exception as e:
            logger.error(f"Error generating LLM response for request ID {request_id}: {e}")
            await self.send_message(
                 MessageType.LLM_RESPONSE,
                 {
                     "request_id": request_id,
                     "status": "failed",
                     "response": f"Error generating response: {str(e)}",
                     "source_documents": [],
                     "trace_id": message.trace_id
                 }
             )