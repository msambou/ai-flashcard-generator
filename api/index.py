import os
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
import openai


# Create FastAPI app
app = FastAPI(title="AI Flashcard Generator API")

# Middleware to strip /api
@app.middleware("http")
async def strip_api_prefix(request, call_next):
    if request.url.path.startswith("/api"):
        request.scope["path"] = request.url.path[4:] or "/"
    return await call_next(request)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Models
class TextInput(BaseModel):
    text: str

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]
    total_count: int

@app.get("/")
async def root():
    return {"message": "AI Flashcard Generator API", "status": "running"}

@app.get("/health")
async def health_check():
    api_key = os.getenv("OPENAI_API_KEY")
    return {
        "status": "healthy" if api_key else "unhealthy",
        "openai_configured": bool(api_key)
    }

@app.post("/generate-flashcards")
async def generate_flashcards(input_data: TextInput):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        if not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Generate flashcards using OpenAI
        prompt = f"""
        Create educational flashcards from the following text. Generate 5-8 flashcards that cover the key concepts.
        
        Text: {input_data.text}
        
        Return the response as a JSON array of objects, each with 'question' and 'answer' fields.
        Make questions clear and concise, and answers comprehensive but not too long.
        
        Example format:
        [
            {{"question": "What is...", "answer": "..."}},
            {{"question": "How does...", "answer": "..."}}
        ]
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        try:
            # Find JSON array in the response
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                flashcards_data = json.loads(json_str)
            else:
                raise ValueError("No JSON array found in response")
        except (json.JSONDecodeError, ValueError):
            # Fallback: create flashcards from text analysis
            flashcards_data = [
                {"question": "What is the main topic of this text?", "answer": input_data.text[:200] + "..."},
                {"question": "What are the key points mentioned?", "answer": "Please review the provided text for detailed information."}
            ]
        
        # Convert to Flashcard objects
        flashcards = [Flashcard(**card) for card in flashcards_data]
        
        logger.info(f"Generated {len(flashcards)} flashcards")
        return FlashcardResponse(flashcards=flashcards, total_count=len(flashcards))
        
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate flashcards: {str(e)}")

handler = app
    
