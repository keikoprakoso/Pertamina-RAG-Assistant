import os
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from rag import RAGSystem
import config

# Initialize FastAPI app
app = FastAPI(title="Company Knowledge Base Assistant", 
              description="RAG-based Q&A system for company SOPs with bilingual support",
              version="1.0.0")

# Initialize RAG system
rag_system = RAGSystem()

# Setup logging
os.makedirs(os.path.dirname(config.LOG_FILE_PATH), exist_ok=True)
logging.basicConfig(
    filename=config.LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    timestamp: str

def log_qa_pair(question: str, answer: str) -> None:
    """Log Q&A pair with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Q: {question} | A: {answer}"
    logging.info(log_entry)

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup"""
    print("Initializing RAG system...")
    if not os.path.exists(config.FAISS_INDEX_PATH):
        print("Building vector store from document...")
        rag_system.build_vector_store("pertamina_sop.txt")
    else:
        print("Loading existing vector store...")
        rag_system.load_vector_store()
    print("RAG system ready!")

@app.get("/")
async def root():
    """Root endpoint - serve the frontend"""
    return {"message": "Company Knowledge Base Assistant API", 
            "status": "active",
            "endpoints": ["/ask", "/docs", "/redoc"]}

@app.get("/ui")
async def frontend_ui():
    """Serve the frontend UI"""
    return {"message": "Frontend UI available at /static/index.html"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Endpoint to ask questions about company SOPs"""
    try:
        # Get answer from RAG system
        answer = rag_system.ask(request.question)
        
        # Log the Q&A pair
        log_qa_pair(request.question, answer)
        
        # Return response
        return AnswerResponse(
            question=request.question,
            answer=answer,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)