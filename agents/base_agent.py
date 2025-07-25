from abc import ABC, abstractmethod
from mcp.protocol import ModelContextProtocol
from mcp.message_types import MCPMessage, MessageType
from utils.logging_config import logger

class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, agent_id: str, message_bus: ModelContextProtocol):
        self.agent_id = agent_id
        self.message_bus = message_bus
        logger.info(f"Agent {self.agent_id} initialized.")

    @abstractmethod
    async def setup(self):
        """Sets up the agent, including registering message handlers."""
        pass

    @abstractmethod
    async def run(self):
        """Runs the agent's main logic."""
        pass

    async def send_message(self, message_or_type, payload=None):
        """Sends a message using the message bus.
        
        This method can be called in two ways:
        1. With an MCPMessage object: send_message(message)
        2. With a MessageType and payload: send_message(MessageType.X, {"key": "value"})
        """
        if payload is not None:
            # Called with message type and payload
            from datetime import datetime
            import uuid
            
            message = MCPMessage(
                sender=self.agent_id,
                receiver="*",  # Broadcast to all
                type=message_or_type,
                trace_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                payload=payload
            )
            await self.message_bus.send_message(message)
        else:
            # Called with MCPMessage object
            await self.message_bus.send_message(message_or_type)

    async def register_handler(self, message_type: MessageType, handler: callable):
        """Registers a message handler with the message bus."""
        await self.message_bus.register_handler(message_type, handler)

    async def _handle_error(self, original_message: MCPMessage, error_code: str, error_message: str, details: str = None):
        """Handles an error by sending an ERROR message back to the sender."""
        error_payload = {
            "code": error_code,
            "message": error_message,
            "details": details
        }
        error_msg = MCPMessage(
            sender=self.agent_id,
            receiver=original_message.sender,
            type=MessageType.ERROR,
            trace_id=original_message.trace_id,
            timestamp=original_message.timestamp, # Use original timestamp for correlation
            payload=error_payload
        )
        await self.send_message(error_msg)
        logger.error(f"Agent {self.agent_id} sent error: {error_message} (Trace ID: {original_message.trace_id})")