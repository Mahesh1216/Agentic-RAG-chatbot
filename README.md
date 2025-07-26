# Agentic RAG Chatbot for Multi-Format Document QA

This project implements an agent-based Retrieval-Augmented Generation (RAG) chatbot capable of answering user questions using uploaded documents of various formats. It leverages a modular, agentic architecture with inter-agent communication facilitated by the Model Context Protocol (MCP).

## Features

- **Multi-Format Document Support**: Processes PDF, PPTX, CSV, DOCX, and TXT/Markdown files.
- **Agentic Architecture**: CoordinatorAgent, IngestionAgent, RetrievalAgent, and LLMAgent for specialized tasks.
- **Model Context Protocol (MCP)**: Structured communication between agents using a defined message schema.
- **Vector Store & Embeddings**: Uses `sentence-transformers` for embeddings and FAISS for efficient similarity search.
- **Streamlit UI**: Intuitive web interface for document upload, chat interaction, and source attribution.
- **Gemini LLM Integration**: Uses Google Gemini models for response generation via API key.

## Project Structure

```
agentic-rag-chatbot/
├── README.md
├── requirements.txt
├── app.py                 # Streamlit main app
├── config/
│   └── settings.py        # Configuration settings
├── agents/
│   ├── base_agent.py      # Base agent class
│   ├── coordinator.py     # Main coordinator agent
│   ├── ingestion_agent.py # Document processing
│   ├── retrieval_agent.py # Vector search & retrieval
│   └── llm_agent.py       # LLM response generation
├── mcp/
│   ├── message_types.py   # MCP message schemas
│   └── protocol.py        # MCP protocol implementation
├── processors/
│   ├── pdf_processor.py   # PDF document handler
│   ├── pptx_processor.py  # PowerPoint handler
│   ├── csv_processor.py   # CSV data handler
│   ├── docx_processor.py  # Word document handler
│   └── text_processor.py  # TXT/MD handler
├── vector_store/
│   ├── faiss_store.py     # FAISS vector database
│   └── embeddings.py      # HuggingFace embeddings
├── ui/
│   ├── components.py      # Streamlit UI components
│   └── chat_interface.py  # Chat UI logic
├── utils/
│   ├── chunking.py        # Text chunking strategies
│   ├── logging_config.py  # Logging setup
│   └── helpers.py         # Utility functions
├── data/
│   ├── uploads/           # User uploaded files
│   ├── vectors/           # FAISS indices
│   └── processed/         # Processed documents
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

4.  **Set up your Gemini API key:**
    - Create a `.env` file in the project root with:
      ```env
      GOOGLE_API_KEY=your_google_gemini_api_key_here
      ```
    - Your API key can be obtained from: https://makersuite.google.com/app/apikey
    - The app uses `python-dotenv` to load this key automatically.

5.  **Configure the LLM model (default: Gemini Flash):**
    - By default, `config/settings.py` uses:
      ```python
      LLM_MODEL_NAME = "models/gemini-1.5-flash-latest"
      ```
    - You may switch to any supported Gemini model listed by your API key.

6.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Usage

- Upload documents through the Streamlit interface.
- Ask questions related to the uploaded documents in the chat.
- The chatbot will retrieve relevant information and generate responses with source citations.

## Environment Variables

- `GOOGLE_API_KEY`: Your Gemini API key (required for LLM responses)

## Troubleshooting

- **Model 404 Error:**
  - Make sure `LLM_MODEL_NAME` in `config/settings.py` matches one of the models listed by your API key (see [Gemini docs](https://ai.google.dev/gemini-api/docs/models)).
  - Example working values: `models/gemini-1.5-flash-latest`, `models/gemini-1.5-pro-latest`.
- **Quota/429 Errors:**
  - You may hit Google’s free-tier or project quota. Wait for reset or upgrade your plan.
  - See your quota at: https://console.cloud.google.com/ai/gemini/quotas
  - Try switching to another model (e.g., Flash vs Pro) for separate quotas.
- **.env Not Loaded:**
  - Ensure `python-dotenv` is installed and `.env` is in the project root.
  - The `.env` file should NOT be committed to version control for security.

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