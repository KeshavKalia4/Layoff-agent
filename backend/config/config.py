import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"

# Data Processing Configuration
EMBEDDING_ENCODING = "cl100k_base"
MAX_TOKENS = 5000
TOP_N_RECORDS = 50

# Vector Search Configuration
VECTOR_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2 embeddings
DEFAULT_K_RESULTS = 5 