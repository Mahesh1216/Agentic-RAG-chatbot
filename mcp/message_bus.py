import asyncio
from collections import defaultdict
from typing import Callable, Dict, Any, List
from mcp.message_types import MCPMessage, MessageType
from mcp.protocol import ModelContextProtocol
from utils.logging_config import logger

class InMemoryMessageBus(ModelContextProtocol):
    """An in-memory implementation of the Model Context Protocol message bus."""

    def __init__(self):
        self._handlers: Dict[MessageType, List[Callable[[MCPMessage], Any]]] = defaultdict(list)
        self._queue: asyncio.Queue[MCPMessage] = asyncio.Queue()
        self._running = False
        self._consumer_task = None

    async def send_message(self, message: MCPMessage):
        """Sends a message by putting it into the queue."""
        await self._queue.put(message)
        logger.info(f"Message sent: {message.type} from {message.sender} to {message.receiver}")

    async def register_handler(self, message_type: MessageType, handler: Callable[[MCPMessage], Any]):
        """Registers a handler for a specific message type."""
        self._handlers[message_type].append(handler)
        logger.info(f"Handler registered for message type: {message_type}")

    async def _consume_messages(self):
        """Continuously consumes messages from the queue and dispatches them to handlers."""
        while self._running:
            try:
                message = await self._queue.get()
                logger.debug(f"Message received from queue: {message.type}")
                if message.type in self._handlers:
                    for handler in self._handlers[message.type]:
                        try:
                            # Handlers can be async or sync
                            if asyncio.iscoroutinefunction(handler):
                                await handler(message)
                            else:
                                handler(message)
                            logger.debug(f"Message {message.type} handled by {handler.__name__}")
                        except Exception as e:
                            logger.error(f"Error handling message {message.type} with handler {handler.__name__}: {e}")
                else:
                    logger.warning(f"No handler registered for message type: {message.type}")
                self._queue.task_done()
            except asyncio.CancelledError:
                logger.info("Message consumer task cancelled.")
                break
            except Exception as e:
                logger.error(f"Error in message consumer: {e}")

    async def start(self):
        """Starts the message bus consumer."""
        if not self._running:
            self._running = True
            self._consumer_task = asyncio.create_task(self._consume_messages())
            logger.info("In-memory message bus started.")

    async def stop(self):
        """Stops the message bus consumer."""
        if self._running:
            self._running = False
            if self._consumer_task:
                self._consumer_task.cancel()
                await self._consumer_task
            logger.info("In-memory message bus stopped.")