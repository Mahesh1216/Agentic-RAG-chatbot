import os

class Settings:
    PROJECT_NAME: str = "Agentic RAG Chatbot"
    PROJECT_VERSION: str = "1.0.0"

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    UPLOAD_DIR: str = os.path.join(DATA_DIR, "uploads")
    PROCESSED_DIR: str = os.path.join(DATA_DIR, "processed")
    VECTOR_STORE_DIR: str = os.path.join(DATA_DIR, "vectors")

    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Embeddings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384 # Dimension for all-MiniLM-L6-v2

    # FAISS
    FAISS_INDEX_NAME: str = "faiss_index"

    # LLM
    LLM_MODEL_NAME = "gemini-pro" # Example, can be changed to other models
    LLM_TEMPERATURE: float = 0.7

    # MCP
    MCP_MESSAGE_BUS_TYPE: str = "in_memory" # or "redis", "kafka" etc.

    # UI
    UI_TITLE: str = "Agentic RAG Chatbot"
    UI_SIDEBAR_TITLE: str = "Navigation"

settings = Settings()