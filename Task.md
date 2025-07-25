# Agentic RAG Chatbot for Multi-Format Document QA

## 🎯 Task Overview
Build an agent-based Retrieval-Augmented Generation (RAG) chatbot that answers user questions using uploaded documents of various formats, implementing Model Context Protocol (MCP) for inter-agent communication.

## 🔧 Core Functional Requirements

### ✅ 1. Document Format Support
- ✅ **PDF** - Extract text and metadata
- [x] PPTX Document Format Support
- - [x] CSV Document Format Support
- [x] DOCX Document Format Support
- [x] TXT/Markdown Document Format Support

### [x] 2. Agentic Architecture (Minimum 3 Agents)

#### [x] **IngestionAgent**
- Parses and preprocesses uploaded documents
- Handles format-specific extraction logic
- Chunks documents for optimal retrieval
- Sends processed content via MCP

#### [x] **RetrievalAgent** 
- Manages document embeddings using HuggingFace models
- Handles semantic search using FAISS vector store
- Retrieves top-k relevant chunks based on user queries
- Communicates results through MCP protocol

#### [x] **LLMResponseAgent**
- Receives context from RetrievalAgent via MCP
- Constructs optimized prompts with retrieved context
- Generates final responses using LLM
- Returns formatted answers with source citations

### ✅ 3. Model Context Protocol (MCP) Implementation
All inter-agent communication must use structured MCP messages:

```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent", 
  "type": "CONTEXT_RESPONSE",
  "trace_id": "abc-123",
  "payload": {
    "top_chunks": ["chunk1", "chunk2"],
    "query": "What are the KPIs?",
    "metadata": {"sources": ["doc1.pdf", "data.csv"]}
  }
}
```

**Implementation Options:**
- In-memory messaging system
- REST API endpoints
- Pub/Sub messaging pattern

### [x] 4. Vector Store & Embeddings
- **Embeddings**: HuggingFace sentence-transformers
- **Vector Database**: FAISS for similarity search
- **Storage**: Persistent vector indices

### [x] 5. User Interface Requirements
**Framework**: Streamlit

**Features**:
- Document upload interface (drag & drop)
- Multi-turn conversation support
- Response display with source context
- Chat history management
- Document management panel

## ✅ 🔄 Sample Workflow

1. **User uploads**: `sales_review.pdf`, `metrics.csv`
2. **User query**: "What KPIs were tracked in Q1?"
3. **Process Flow**:
   ```
   UI → CoordinatorAgent → IngestionAgent (parse docs)
                        → RetrievalAgent (find chunks) 
                        → LLMResponseAgent (generate answer)
                        → UI (display with sources)
   ```

## ✅ 📋 MCP Message Types

### Message Schema
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
- `INGESTION_REQUEST` - Trigger document processing
- `INGESTION_COMPLETE` - Document processing finished
- `RETRIEVAL_REQUEST` - Request semantic search
- `RETRIEVAL_RESULT` - Return search results
- `LLM_REQUEST` - Request response generation
- `LLM_RESPONSE` - Return generated answer

## ✅ 🛠 Tech Stack
- **Frontend**: Streamlit
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace sentence-transformers
- **Document Processing**: PyPDF2, python-pptx, pandas, python-docx
- **LLM Integration**: Multiple options (OpenAI, HuggingFace, etc.)
- **MCP Implementation**: Custom Python messaging system

## ✅ 📦 Deliverables

### 1. GitHub Repository
- Well-organized, modular code structure
- Comprehensive README.md with setup instructions
- Requirements.txt with all dependencies
- Docker configuration (optional)
- ✅ Create `config/settings.py` for configuration management.
- ✅ Implement logging configuration in `utils/logging_config.py`.
- ✅ Implement utility functions in `utils/helpers.py`.
- ✅ Implement text chunking logic in `utils/chunking.py`.
- ✅ Define MCP message types and schemas in `mcp/message_types.py`.
- ✅ Implement the core MCP protocol in `mcp/protocol.py`.
- ✅ Implement an in-memory message bus in `mcp/message_bus.py`.
- ✅ Implement the `BaseAgent` class in `agents/base_agent.py`.
- ✅ Implement the `Coordinator` agent in `agents/coordinator.py`.
- [x] Embedding Model Implementation
- [x] Vector Store Implementation (FAISS)
- [x] Chat Interface (main application logic)

### 2. Architecture Presentation (3-6 slides)
- Agent-based architecture diagram
- System flow with MCP message passing
- Tech stack overview
- UI screenshots
- Challenges and solutions
- Future improvements

### 3. Demo Video (5 minutes)
- 1 min: Application demonstration
- 2 min: Architecture and flow explanation  
- 2 min: Code walkthrough
- Face-on-camera optional

## ✅ 🎯 Success Criteria
- ✅ Multi-format document support working
- ✅ All 3+ agents communicating via MCP
- ✅ Semantic retrieval returning relevant results
- ✅ Clean, intuitive Streamlit interface
- ✅ Proper source attribution in responses
- ✅ Multi-turn conversation capability