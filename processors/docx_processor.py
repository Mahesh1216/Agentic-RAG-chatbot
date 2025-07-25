import logging
from docx import Document
from config.settings import settings
from utils.chunking import chunk_text

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP

logger = logging.getLogger(__name__)

class DOCXProcessor:
    """
    A processor for extracting text from DOCX documents and chunking it.
    """
    def __init__(self):
        """
        Initializes the DOCXProcessor.
        """
        logger.info("DOCXProcessor initialized.")

    def process(self, file_path: str) -> list[str]:
        """
        Extracts text from a DOCX file, chunks it, and returns a list of text chunks.

        Args:
            file_path (str): The path to the DOCX file.

        Returns:
            list[str]: A list of text chunks extracted from the DOCX.
        """
        try:
            document = Document(file_path)
            full_text = []
            for paragraph in document.paragraphs:
                full_text.append(paragraph.text)
            
            combined_text = "\n".join(full_text)
            chunks = chunk_text(combined_text, CHUNK_SIZE, CHUNK_OVERLAP)
            logger.info(f"Successfully processed DOCX file: {file_path}. Extracted {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {e}")
            return []