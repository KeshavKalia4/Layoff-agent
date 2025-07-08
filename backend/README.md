# Layoff RAG Backend

This is the backend service for the Layoff RAG application. It provides a REST API for querying layoff data using RAG (Retrieval Augmented Generation) with Claude and FAISS.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with your API keys:
```
ANTHROPIC_API_KEY=your_api_key_here
DATA_PATH=path/to/your/layoffs.csv
```

## Running the Service

Start the FastAPI server:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Query Layoffs
- **POST** `/query`
- Body:
```json
{
    "text": "Which companies in United Kingdom laid off employees recently?",
    "k": 5
}
```

### Health Check
- **GET** `/health`

## Project Structure

- `api/` - FastAPI application and RAG service
- `config/` - Configuration settings
- `data/` - Data processing utilities
- `models/` - Embedding model
- `vector_db/` - FAISS vector database
- `utils/` - Utility functions

## Dependencies

- FastAPI
- Anthropic
- FAISS
- Sentence Transformers
- Pandas
- NumPy 