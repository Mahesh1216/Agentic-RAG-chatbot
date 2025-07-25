from typing import List
from config.settings import settings

def chunk_text(text: str, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP) -> List[str]:
    """Chunks a given text into smaller pieces with a specified overlap."""
    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be less than chunk size.")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks