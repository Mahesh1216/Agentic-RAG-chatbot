import logging
from config.settings import settings
from utils.chunking import chunk_text

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP

logger = logging.getLogger(__name__)

class TextProcessor:
    """
    A processor for extracting text from plain text and Markdown documents and chunking it.
    """
    def __init__(self):
        """
        Initializes the TextProcessor.
        """
        logger.info("TextProcessor initialized.")

    def process(self, file_path: str) -> list[str]:
        """
        Extracts text from a plain text or Markdown file, chunks it, and returns a list of text chunks.

        Args:
            file_path (str): The path to the text/Markdown file.

        Returns:
            list[str]: A list of text chunks extracted from the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                full_text = f.read()
            
            chunks = chunk_text(full_text, CHUNK_SIZE, CHUNK_OVERLAP)
            logger.info(f"Successfully processed text file: {file_path}. Extracted {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return []