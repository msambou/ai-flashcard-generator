export interface Flashcard {
  question: string
  answer: string
}

export interface FlashcardResponse {
  flashcards: Flashcard[]
  total_count: number
}

export interface ApiError {
  detail: string
  error_code?: string
}
