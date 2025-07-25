import logging
import faiss
import numpy as np
import os
from config.settings import settings
from vector_store.embeddings import EmbeddingModel

logger = logging.getLogger(__name__)

class FAISSVectorStore:
    """
    A FAISS-based vector store for efficient similarity search.
    """
    def __init__(self):
        """
        Initializes the FAISSVectorStore, loading an existing index if available,
        or creating a new one.
        """
        self.index = None
        self.texts = []
        self.embedding_model = EmbeddingModel()
        self.index_path = os.path.join(settings.VECTOR_STORE_DIR, settings.FAISS_INDEX_NAME)
        self._load_or_create_index()
        logger.info("FAISSVectorStore initialized.")

    def _load_or_create_index(self):
        """
        Loads the FAISS index and texts from disk if they exist, otherwise creates a new index.
        """
        if os.path.exists(self.index_path) and os.path.exists(self.index_path + ".texts"):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.index_path + ".texts", "r", encoding="utf-8") as f:
                    self.texts = [line.strip() for line in f]
                logger.info(f"FAISS index and texts loaded from {self.index_path}")
            except Exception as e:
                logger.error(f"Error loading FAISS index or texts: {e}. Creating new index.")
                self._create_new_index()
        else:
            logger.info("No existing FAISS index found. Creating a new one.")
            self._create_new_index()

    def _create_new_index(self):
        """
        Creates a new FAISS index.
        """
        self.index = faiss.IndexFlatL2(settings.EMBEDDING_DIMENSION)  # L2 distance for similarity
        self.texts = []
        logger.info(f"New FAISS index created with dimension {settings.EMBEDDING_DIMENSION}")

    def add_documents(self, documents: list[str]):
        """
        Adds a list of text documents to the FAISS index.

        Args:
            documents (list[str]): A list of text documents to add.
        """
        if not documents:
            return

        new_embeddings = self.embedding_model.get_embeddings(documents)
        if not new_embeddings:
            logger.error("Could not generate embeddings for documents. Aborting add.")
            return

        new_embeddings_np = np.array(new_embeddings).astype('float32')

        if self.index.is_trained:
            self.index.add(new_embeddings_np)
        else:
            # For IndexFlatL2, is_trained is always true after creation, but good practice
            # to handle other index types that might require training.
            self.index.add(new_embeddings_np)

        self.texts.extend(documents)
        logger.info(f"Added {len(documents)} documents to FAISS index. Total documents: {len(self.texts)}")
        self._save_index()

    def search(self, query: str, k: int = 5) -> list[str]:
        """
        Searches the FAISS index for the top-k most similar documents to the query.

        Args:
            query (str): The query string.
            k (int): The number of nearest neighbors to retrieve.

        Returns:
            list[str]: A list of the top-k most similar text documents.
        """
        if not self.index or self.index.ntotal == 0:
            logger.warning("FAISS index is empty. No search performed.")
            return []

        query_embedding = self.embedding_model.get_embeddings([query])
        if not query_embedding:
            logger.error("Could not generate embedding for query. Aborting search.")
            return []

        query_embedding_np = np.array(query_embedding).astype('float32')

        D, I = self.index.search(query_embedding_np, k)  # D is distances, I is indices

        results = []
        for i in I[0]:
            if i != -1 and i < len(self.texts):  # Ensure index is valid
                results.append(self.texts[i])
        
        logger.info(f"Performed FAISS search for query. Found {len(results)} results.")
        return results

    def _save_index(self):
        """
        Saves the FAISS index and associated texts to disk.
        """
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.index_path + ".texts", "w", encoding="utf-8") as f:
                for text in self.texts:
                    f.write(text + "\n")
            logger.info(f"FAISS index and texts saved to {self.index_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index or texts: {e}")

    def clear_index(self):
        """
        Clears the FAISS index and removes associated files from disk.
        """
        self._create_new_index() # Re-initialize an empty index
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.index_path + ".texts"):
            os.remove(self.index_path + ".texts")
        logger.info("FAISS index and associated files cleared.")