from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

from .models import TextInput, FlashcardResponse, ErrorResponse
from .services.flashcard_service import FlashcardService
from .services.openai_service import OpenAIService
from .config import settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize services
def get_openai_service():
    api_key = settings.openai_api_key
    if not api_key:
        logger.error("OpenAI API key not configured")
        raise HTTPException(status_code=500, detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
    return OpenAIService(api_key)

def get_flashcard_service(openai_service: OpenAIService = Depends(get_openai_service)):
    return FlashcardService(openai_service)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

@app.get("/")
async def root():
    return {
        "message": "AI Flashcard Generator API", 
        "version": settings.api_version,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if OpenAI API key is configured
        api_key = settings.openai_api_key
        if not api_key:
            return {"status": "unhealthy", "reason": "OpenAI API key not configured"}
        
        return {
            "status": "healthy", 
            "version": settings.api_version,
            "openai_configured": bool(api_key)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "reason": str(e)}

@app.post("/generate-flashcards", response_model=FlashcardResponse)
async def generate_flashcards(
    input_data: TextInput,
    flashcard_service: FlashcardService = Depends(get_flashcard_service)
):
    """Generate flashcards from input text using AI"""
    try:
        logger.info(f"Generating flashcards for text of length: {len(input_data.text)}")
        
        # Validate input
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
        if len(input_data.text) > 10000:
            raise HTTPException(status_code=400, detail="Text input too long (max 10,000 characters)")
        
        # Generate flashcards
        flashcards = await flashcard_service.generate_flashcards(input_data.text)
        
        logger.info(f"Successfully generated {len(flashcards)} flashcards")
        return FlashcardResponse(flashcards=flashcards, total_count=len(flashcards))
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate flashcards. Please try again.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.reload
    )
