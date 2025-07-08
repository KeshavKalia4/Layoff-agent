import os
import anthropic
from backend.config.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, DEFAULT_K_RESULTS
from backend.data.processor import DataProcessor
from backend.models.embedder import Embedder
from backend.vector_db.faiss_index import FAISSIndex

class RAGService:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.embedder = Embedder()
        self.vector_index = FAISSIndex()
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.df = None
        self.is_initialized = False
        
    def initialize(self, data_path):
        """Initialize the RAG service with data."""
        try:
            # Process data
            self.df = self.data_processor.load_and_preprocess(data_path)
            
            # Generate embeddings
            embeddings = self.embedder.get_embeddings_batch(self.df["combined"].tolist())
            
            # Add to vector index
            self.vector_index.add_embeddings(embeddings)
            self.is_initialized = True
            print(f"Successfully initialized RAG service with {len(self.df)} records")
        except Exception as e:
            print(f"Error initializing RAG service: {str(e)}")
            raise
    
    def search_layoffs(self, query_text, k=DEFAULT_K_RESULTS):
        """Search for relevant layoff records."""
        if not self.is_initialized or self.df is None:
            raise ValueError("RAG service not initialized. Please initialize with data first.")
            
        # Get query embedding
        query_vec = self.embedder.get_embedding(query_text)
        
        # Search
        distances, indices = self.vector_index.search(query_vec, k)
        
        # Get results
        results = self.df.iloc[indices][["combined", "Company", "Date", "Industry", "Location HQ"]]
        return results
    
    def generate_response(self, query, k=DEFAULT_K_RESULTS):
        """Generate a response using Claude with RAG."""
        if not self.is_initialized or self.df is None:
            raise ValueError("RAG service not initialized. Please initialize with data first.")
            
        # Get relevant documents
        relevant_docs = self.search_layoffs(query, k)
        context = "\n---\n".join(relevant_docs["combined"].tolist()[:3])
        
        # Create system prompt
        system_prompt = f"""
You are a helpful assistant that answers user queries based on historical tech layoff events.

Use the following context (layoff reports) to answer the question.
If the context does not contain enough information, you may answer from your own knowledge.

Context:
{context}
"""
        
        # Generate response
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            system=system_prompt.strip(),
            messages=[{"role": "user", "content": query}],
            temperature=0.3,
            max_tokens=300
        )
        print("DEBUG: Claude response.content type:", type(response.content))
        print("DEBUG: Claude response.content value:", response.content)
        if isinstance(response.content, list):
            text = "".join([getattr(block, "text", "") for block in response.content if getattr(block, "type", None) == "text"])
            return text
        elif hasattr(response.content, "text"):
            return str(response.content.text)
        return str(response.content) 