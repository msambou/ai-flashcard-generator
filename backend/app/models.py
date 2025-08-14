from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class TextInput(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000, description="Text content to generate flashcards from")
    
    @validator('text')
    def validate_text(cls, v):
        # Remove excessive whitespace
        v = re.sub(r'\s+', ' ', v.strip())
        if len(v) < 10:
            raise ValueError('Text must be at least 10 characters long')
        return v

class Flashcard(BaseModel):
    question: str = Field(..., min_length=5, max_length=500, description="The question for the flashcard")
    answer: str = Field(..., min_length=1, max_length=1000, description="The answer for the flashcard")
    
    @validator('question', 'answer')
    def validate_content(cls, v):
        return v.strip()

class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard] = Field(..., min_items=1, max_items=15)
    total_count: int = Field(..., description="Total number of flashcards generated")
    
    @validator('total_count', always=True)
    def set_total_count(cls, v, values):
        if 'flashcards' in values:
            return len(values['flashcards'])
        return v

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
