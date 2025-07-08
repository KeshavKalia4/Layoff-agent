import numpy as np
from collections import Counter
import math

class Embedder:
    def __init__(self):
        self.word_frequencies = {}
        self.document_count = 0
        
    def _compute_tfidf(self, text):
        """Compute TF-IDF vector for a text."""
        # Tokenize (simple split by space)
        words = text.lower().split()
        
        # Compute term frequencies
        word_counts = Counter(words)
        
        # Create TF-IDF vector
        vector = np.zeros(384)  # Using 384 dimensions to match original
        for i, (word, count) in enumerate(word_counts.most_common(384)):
            if i >= 384:
                break
            # Simple TF-IDF calculation
            tf = count / len(words)
            idf = math.log((self.document_count + 1) / (self.word_frequencies.get(word, 0) + 1))
            vector[i] = tf * idf
            
        return vector
    
    def get_embedding(self, text):
        """Generate embedding for a given text."""
        return self._compute_tfidf(text)
    
    def get_embeddings_batch(self, texts):
        """Generate embeddings for a batch of texts."""
        # Update word frequencies
        for text in texts:
            words = text.lower().split()
            for word in set(words):
                self.word_frequencies[word] = self.word_frequencies.get(word, 0) + 1
            self.document_count += 1
            
        # Generate embeddings
        return np.array([self._compute_tfidf(text) for text in texts]) 