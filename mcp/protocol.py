from abc import ABC, abstractmethod
from typing import Callable, Dict, Any
from mcp.message_types import MCPMessage, MessageType

class ModelContextProtocol(ABC):
    """Abstract base class for the Model Context Protocol."""

    @abstractmethod
    async def send_message(self, message: MCPMessage):
        """Sends a message through the protocol."""
        pass

    @abstractmethod
    async def register_handler(self, message_type: MessageType, handler: Callable[[MCPMessage], Any]):
        """Registers a handler for a specific message type."""
        pass

    @abstractmethod
    async def start(self):
        """Starts the protocol's message processing."""
        pass

    @abstractmethod
    async def stop(self):
        """Stops the protocol's message processing."""
        pass