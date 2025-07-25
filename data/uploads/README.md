# Agentic RAG Chatbot for Multi-Format Document QA

This project implements an agent-based Retrieval-Augmented Generation (RAG) chatbot capable of answering user questions using uploaded documents of various formats. It leverages a modular, agentic architecture with inter-agent communication facilitated by the Model Context Protocol (MCP).

## Features

- **Multi-Format Document Support**: Processes PDF, PPTX, CSV, DOCX, and TXT/Markdown files.
- **Agentic Architecture**: Comprises IngestionAgent, RetrievalAgent, and LLMResponseAgent for specialized tasks.
- **Model Context Protocol (MCP)**: Structured communication between agents using a defined message schema.
- **Vector Store & Embeddings**: Utilizes HuggingFace `sentence-transformers` for embeddings and FAISS for efficient similarity search.
- **Streamlit UI**: Provides an intuitive web interface for document upload, chat interaction, and source attribution.

## Project Structure

```
agentic-rag-chatbot/
├── README.md
├── requirements.txt
├── app.py                 # Streamlit main app
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration settings
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── coordinator.py     # Main coordinator agent
│   ├── ingestion_agent.py # Document processing
│   ├── retrieval_agent.py # Vector search & retrieval
│   └── llm_agent.py       # LLM response generation
├── mcp/
│   ├── __init__.py
│   ├── message_types.py   # MCP message schemas
│   ├── message_bus.py     # In-memory message passing
│   └── protocol.py        # MCP protocol implementation
├── processors/
│   ├── __init__.py
│   ├── pdf_processor.py   # PDF document handler
│   ├── pptx_processor.py  # PowerPoint handler
│   ├── csv_processor.py   # CSV data handler
│   ├── docx_processor.py  # Word document handler
│   └── text_processor.py  # TXT/MD handler
├── vector_store/
│   ├── __init__.py
│   ├── faiss_store.py     # FAISS vector database
│   └── embeddings.py      # HuggingFace embeddings
├── ui/
│   ├── __init__.py
│   ├── components.py      # Streamlit UI components
│   └── chat_interface.py  # Chat UI logic
├── utils/
│   ├── __init__.py
│   ├── chunking.py        # Text chunking strategies
│   ├── logging_config.py  # Logging setup
│   └── helpers.py         # Utility functions
├── data/
│   ├── uploads/           # User uploaded files
│   ├── vectors/           # FAISS indices
│   └── processed/         # Processed documents
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_mcp.py
│   └── test_processors.py
├── docs/
│   ├── architecture.pptx  # Architecture presentation
│   └── demo_video.mp4     # Demo video
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd agentic-rag-chatbot
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Usage

-   Upload documents through the Streamlit interface.
-   Ask questions related to the uploaded documents in the chat.
-   The chatbot will retrieve relevant information and generate responses with source citations.

## MCP Message Structure

All inter-agent communication adheres to the following MCP message schema:

```json
{
  "type": "MESSAGE_TYPE",
  "sender": "AgentName", 
  "receiver": "AgentName",
  "trace_id": "unique-id",
  "timestamp": "ISO-timestamp",
  "payload": {}
}
```

### Message Types

-   `INGESTION_REQUEST`: Trigger document processing.
-   `INGESTION_COMPLETE`: Document processing finished.
-   `RETRIEVAL_REQUEST`: Request semantic search.
-   `RETRIEVAL_RESULT`: Return search results.
-   `LLM_REQUEST`: Request response generation.
-   `LLM_RESPONSE`: Return generated answer.

## Contributing

Contributions are welcome! Please follow the standard fork-and-pull request workflow.

## License

This project is licensed under the MIT License.