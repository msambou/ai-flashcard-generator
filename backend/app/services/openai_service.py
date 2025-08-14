import openai
import json
import logging
import asyncio
from typing import List, Dict, Any
from ..models import Flashcard

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        
    async def generate_flashcards_from_text(self, text: str, num_cards: int = 6) -> List[Flashcard]:
        """Generate flashcards from text using OpenAI API"""
        try:
            prompt = self._create_flashcard_prompt(text, num_cards)
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are an expert educational content creator. Generate high-quality flashcards that test comprehension, analysis, and key concepts. Always respond with valid JSON only."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500,
                    response_format={"type": "json_object"}
                )
            )
            
            # Parse response
            content = response.choices[0].message.content
            logger.info(f"OpenAI response received: {len(content)} characters")
            
            flashcards_data = json.loads(content)
            
            # Handle different response formats
            if "flashcards" in flashcards_data:
                cards_list = flashcards_data["flashcards"]
            elif isinstance(flashcards_data, list):
                cards_list = flashcards_data
            else:
                raise ValueError("Unexpected response format from OpenAI")
            
            # Convert to Flashcard objects with validation
            flashcards = []
            for card_data in cards_list:
                if isinstance(card_data, dict) and "question" in card_data and "answer" in card_data:
                    flashcard = Flashcard(
                        question=card_data["question"].strip(),
                        answer=card_data["answer"].strip()
                    )
                    flashcards.append(flashcard)
            
            if not flashcards:
                raise ValueError("No valid flashcards generated")
                
            logger.info(f"Successfully parsed {len(flashcards)} flashcards")
            return flashcards
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("Failed to parse AI response as JSON")
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise ValueError(f"Failed to generate flashcards: {str(e)}")
    
    def _create_flashcard_prompt(self, text: str, num_cards: int) -> str:
        """Create a well-structured prompt for flashcard generation"""
        return f"""
        Create exactly {num_cards} educational flashcards based on the following text. 
        
        Requirements:
        - Focus on key concepts, definitions, and important facts
        - Questions should test understanding, not just memorization
        - Include a mix of question types (what, how, why, when, where)
        - Keep questions clear and concise (under 100 words)
        - Provide complete, accurate answers (under 200 words)
        - Ensure questions and answers are directly related to the text content
        - Make questions challenging but fair
        
        Text to analyze:
        {text}
        
        Respond with a JSON object in this exact format:
        {{
            "flashcards": [
                {{"question": "Clear, specific question here?", "answer": "Complete, accurate answer here."}},
                {{"question": "Another question?", "answer": "Another answer."}}
            ]
        }}
        """
