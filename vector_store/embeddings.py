import logging
from sentence_transformers import SentenceTransformer
from config.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """
    A wrapper for the SentenceTransformer model to generate text embeddings.
    """
    def __init__(self):
        """
        Initializes the EmbeddingModel by loading the pre-trained SentenceTransformer.
        """
        try:
            # Explicitly set device to CPU to avoid meta tensor issues
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME, device="cpu")
            logger.info(f"Embedding model '{settings.EMBEDDING_MODEL_NAME}' loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading embedding model {settings.EMBEDDING_MODEL_NAME}: {e}")
            self.model = None

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a list of text strings.

        Args:
            texts (list[str]): A list of text strings to embed.

        Returns:
            list[list[float]]: A list of embeddings, where each embedding is a list of floats.
        """
        if not self.model:
            logger.error("Embedding model not loaded. Cannot generate embeddings.")
            return []
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=False).tolist()
            logger.info(f"Generated embeddings for {len(texts)} texts.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []