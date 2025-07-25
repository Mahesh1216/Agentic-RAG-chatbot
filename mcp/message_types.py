from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class MessageType(str, Enum):
    INGESTION_REQUEST = "INGESTION_REQUEST"
    INGESTION_RESPONSE = "INGESTION_RESPONSE"
    INGESTION_COMPLETE = "INGESTION_COMPLETE"
    RETRIEVAL_REQUEST = "RETRIEVAL_REQUEST"
    RETRIEVAL_RESULT = "RETRIEVAL_RESULT"
    LLM_REQUEST = "LLM_REQUEST"
    LLM_RESPONSE = "LLM_RESPONSE"
    ERROR = "ERROR"

class MCPMessage(BaseModel):
    sender: str
    receiver: str
    type: MessageType
    trace_id: str
    timestamp: str # ISO format string
    payload: Dict[str, Any]

class IngestionRequestPayload(BaseModel):
    file_path: str
    file_type: str
    document_id: str

class IngestionResponsePayload(BaseModel):
    request_id: str
    status: str
    message: str

class IngestionCompletePayload(BaseModel):
    document_id: str
    status: str
    message: Optional[str] = None
    processed_chunks: Optional[int] = None

class RetrievalRequestPayload(BaseModel):
    query: str
    top_k: int = 5
    document_ids: Optional[List[str]] = None

class RetrievalResultPayload(BaseModel):
    query: str
    top_chunks: List[str]
    metadata: Dict[str, Any]
    document_id: Optional[str] = None

class LLMRequestPayload(BaseModel):
    query: str
    context: List[str]
    chat_history: Optional[List[Dict[str, str]]] = None

class LLMResponsePayload(BaseModel):
    response: str
    source_documents: List[Dict[str, Any]]
    trace_id: str

class ErrorPayload(BaseModel):
    code: str
    message: str
    details: Optional[str] = None