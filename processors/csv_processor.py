import logging
import pandas as pd
from config.settings import settings
from utils.chunking import chunk_text

CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP

logger = logging.getLogger(__name__)

class CSVProcessor:
    """
    A processor for extracting text from CSV documents and chunking it.
    """
    def __init__(self):
        """
        Initializes the CSVProcessor.
        """
        logger.info("CSVProcessor initialized.")

    def process(self, file_path: str) -> list[str]:
        """
        Extracts text from a CSV file, chunks it, and returns a list of text chunks.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            list[str]: A list of text chunks extracted from the CSV.
        """
        try:
            df = pd.read_csv(file_path)
            # Convert all columns to string to ensure consistent text extraction
            full_text = df.to_string(index=False)
            
            chunks = chunk_text(full_text, CHUNK_SIZE, CHUNK_OVERLAP)
            logger.info(f"Successfully processed CSV file: {file_path}. Extracted {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
            return []