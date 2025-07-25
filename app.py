import asyncio
from ui.chat_interface import ChatInterface

async def main():
    chat_interface = ChatInterface()
    await chat_interface.setup_agents()
    await chat_interface.run()

if __name__ == "__main__":
    asyncio.run(main())