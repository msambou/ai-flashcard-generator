from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from dotenv import load_dotenv

from .models import TextInput, FlashcardResponse
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

# Create FastAPI app
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

# Dependencies
def get_openai_service():
    api_key = settings.openai_api_key
    if not api_key:
        logger.error("OpenAI API key not configured")
        raise HTTPException(status_code=500, detail="OpenAI API key not configured.")
    return OpenAIService(api_key)

def get_flashcard_service(openai_service: OpenAIService = Depends(get_openai_service)):
    return FlashcardService(openai_service)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error occurred"})

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AI Flashcard Generator API", "version": settings.api_version, "docs": "/docs"}

# Health check endpoint
@app.get("/health")
async def health_check():
    api_key = settings.openai_api_key
    return {"status": "healthy" if api_key else "unhealthy", "openai_configured": bool(api_key)}

# Generate flashcards endpoint
@app.post("/generate-flashcards", response_model=FlashcardResponse)
async def generate_flashcards(
    input_data: TextInput,
    flashcard_service: FlashcardService = Depends(get_flashcard_service)
):
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    if len(input_data.text) > 10000:
        raise HTTPException(status_code=400, detail="Text input too long (max 10,000 characters)")
    try:
        flashcards = await flashcard_service.generate_flashcards(input_data.text)
        logger.info(f"Generated {len(flashcards)} flashcards")
        return FlashcardResponse(flashcards=flashcards, total_count=len(flashcards))
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate flashcards. Please try again.")

# Only for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.reload)
