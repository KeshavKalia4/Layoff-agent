import numpy as np

class FAISSIndex:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.embeddings = None
        
    def add_embeddings(self, embeddings):
        """Add embeddings to the index."""
        self.embeddings = np.array(embeddings, dtype=np.float32)
        
    def _cosine_similarity(self, a, b):
        """Compute cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
    def search(self, query_vector, k=5):
        """Search for similar vectors using cosine similarity."""
        if self.embeddings is None:
            return np.array([]), np.array([])
            
        # Compute cosine similarity with all embeddings
        similarities = np.array([self._cosine_similarity(query_vector, emb) for emb in self.embeddings])
        
        # Get top k indices
        indices = np.argsort(similarities)[-k:][::-1]
        distances = similarities[indices]
        
        return distances, indices 