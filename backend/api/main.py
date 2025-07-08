from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from .rag_service import RAGService
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Layoff RAG API",
    description="API for querying layoff data using RAG (Retrieval Augmented Generation)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()
DATA_PATH = os.getenv("DATA_PATH", "data/Layoffs.csv")

@app.on_event("startup")
def startup_event():
    try:
        rag_service.initialize(DATA_PATH)
        print(f"Successfully initialized RAG service with data from {DATA_PATH}")
    except Exception as e:
        print(f"Error initializing RAG service: {str(e)}")
        raise

class Query(BaseModel):
    text: str
    k: int = 5

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Layoff RAG API",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Query the layoff database using RAG",
            "/health": "GET - Health check endpoint",
            "/search": "GET - Search layoffs",
            "/ask": "GET - Ask a question"
        }
    }

@app.post("/query")
async def query_layoffs(query: Query):
    """Query the layoff database using RAG."""
    try:
        response = rag_service.generate_response(query.text, query.k)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/search")
def search(query: str, k: int = 5):
    results = rag_service.search_layoffs(query, k)
    return results.to_dict(orient="records")

@app.get("/ask")
def ask(query: str, k: int = 5):
    answer = rag_service.generate_response(query, k)
    # If answer is a list of objects, extract the text from the first one
    if isinstance(answer, list) and len(answer) > 0 and isinstance(answer[0], dict) and "text" in answer[0]:
        answer = answer[0]["text"]
    return {"answer": answer} 