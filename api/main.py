from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LLM-InfraLite API",
    description="A lightweight LLM inference API service",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class ChatRequest(BaseModel):
    prompt: str
    model: str = "qwen:3b"  # Default model
    stream: bool = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.7

class ModelListRequest(BaseModel):
    pass

# Environment variables
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# Helper functions
async def call_ollama_api(endpoint: str, json_data: Dict[str, Any]):
    """Call Ollama API with the given endpoint and JSON data"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            url = f"{OLLAMA_API_BASE}/api/{endpoint}"
            logger.info(f"Calling Ollama API: {url}")
            response = await client.post(url, json=json_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Ollama API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to LLM-InfraLite API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Process a chat request and return the model's response"""
    try:
        logger.info(f"Processing chat request with model: {request.model}")
        
        # Prepare request for Ollama
        ollama_request = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": request.stream
        }
        
        # Add optional parameters if provided
        if request.max_tokens:
            ollama_request["max_tokens"] = request.max_tokens
        if request.temperature:
            ollama_request["temperature"] = request.temperature
        
        # Call Ollama API
        result = await call_ollama_api("generate", ollama_request)
        
        return {
            "model": request.model,
            "response": result.get("response", ""),
            "total_tokens": result.get("total_tokens", 0),
        }
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models from Ollama"""
    try:
        result = await call_ollama_api("tags", {})
        return {"models": result.get("models", [])}
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Add Prometheus metrics if available
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    instrumentator = Instrumentator().instrument(app)
    instrumentator.expose(app)
    logger.info("Prometheus metrics enabled at /metrics")
except ImportError:
    logger.info("Prometheus metrics not enabled (prometheus_fastapi_instrumentator not installed)")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
