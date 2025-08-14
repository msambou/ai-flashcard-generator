import logging
from typing import List
from .openai_service import OpenAIService
from ..models import Flashcard

logger = logging.getLogger(__name__)

class FlashcardService:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
    
    async def generate_flashcards(self, text: str) -> List[Flashcard]:
        """Generate flashcards from input text"""
        try:
            # Determine optimal number of flashcards based on text length
            num_cards = self._calculate_optimal_card_count(text)
            
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            # Generate flashcards using OpenAI
            flashcards = await self.openai_service.generate_flashcards_from_text(
                processed_text, num_cards
            )
            
            # Post-process and validate flashcards
            validated_flashcards = self._validate_flashcards(flashcards)
            
            return validated_flashcards
            
        except Exception as e:
            logger.error(f"Error in flashcard generation: {e}")
            raise
    
    def _calculate_optimal_card_count(self, text: str) -> int:
        """Calculate optimal number of flashcards based on text length"""
        word_count = len(text.split())
        
        if word_count < 100:
            return 3
        elif word_count < 300:
            return 5
        elif word_count < 600:
            return 7
        elif word_count < 1000:
            return 9
        else:
            return 12
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess input text"""
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove very short lines that might be artifacts
        lines = text.split('\n')
        meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return '\n'.join(meaningful_lines)
    
    def _validate_flashcards(self, flashcards: List[Flashcard]) -> List[Flashcard]:
        """Validate and filter flashcards"""
        validated = []
        
        for card in flashcards:
            # Skip cards with very short questions or answers
            if len(card.question) < 10 or len(card.answer) < 5:
                continue
                
            # Skip duplicate questions
            if any(existing.question.lower() == card.question.lower() for existing in validated):
                continue
                
            validated.append(card)
        
        # Ensure we have at least one flashcard
        if not validated and flashcards:
            validated = flashcards[:1]  # Take at least the first one
            
        return validated
