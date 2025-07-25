from typing import List
from PyPDF2 import PdfReader
from utils.chunking import chunk_text
from utils.logging_config import logger
from config.settings import settings

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP

class PDFProcessor:
    """Processes PDF documents to extract text and chunk it."""

    def __init__(self):
        logger.info("PDFProcessor initialized.")

    def process(self, file_path: str) -> List[str]:
        """Extracts text from a PDF and returns a list of text chunks."""
        text_content = self._extract_text_from_pdf(file_path)
        chunks = chunk_text(text_content)
        logger.info(f"Processed PDF: {file_path}, extracted {len(chunks)} chunks.")
        return chunks

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Helper to extract all text from a PDF file."""
        full_text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    full_text += page.extract_text() or ""
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            raise
        return full_text