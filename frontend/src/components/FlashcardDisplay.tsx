"use client"

import type React from "react"
import { useState } from "react"
import { ChevronLeft, ChevronRight, RotateCcw, RefreshCw } from "lucide-react"
import type { Flashcard } from "../types"

interface FlashcardDisplayProps {
  flashcards: Flashcard[]
  onReset: () => void
}

export const FlashcardDisplay: React.FC<FlashcardDisplayProps> = ({ flashcards, onReset }) => {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  const currentCard = flashcards[currentIndex]

  const nextCard = () => {
    setCurrentIndex((prev) => (prev + 1) % flashcards.length)
    setIsFlipped(false)
  }

  const prevCard = () => {
    setCurrentIndex((prev) => (prev - 1 + flashcards.length) % flashcards.length)
    setIsFlipped(false)
  }

  const flipCard = () => {
    setIsFlipped(!isFlipped)
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 font-serif">Your Flashcards</h2>
          <p className="text-slate-600">
            {flashcards.length} cards generated • Card {currentIndex + 1} of {flashcards.length}
          </p>
        </div>
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-4 py-2 text-slate-600 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          New Cards
        </button>
      </div>

      {/* Flashcard */}
      <div className="relative mb-8">
        <div
          className="bg-white rounded-xl shadow-lg border border-slate-200 min-h-[300px] cursor-pointer transform transition-transform hover:scale-[1.02]"
          onClick={flipCard}
        >
          <div className="p-8 h-full flex flex-col justify-center">
            <div className="text-center">
              <div className="mb-4">
                <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                  {isFlipped ? "Answer" : "Question"}
                </span>
              </div>
              <div className="text-lg leading-relaxed text-slate-800">
                {isFlipped ? currentCard.answer : currentCard.question}
              </div>
            </div>
          </div>

          {/* Flip indicator */}
          <div className="absolute bottom-4 right-4">
            <div className="flex items-center gap-1 text-slate-400 text-sm">
              <RotateCcw className="w-4 h-4" />
              Click to flip
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={prevCard}
          disabled={flashcards.length <= 1}
          className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 disabled:bg-slate-50 disabled:text-slate-400 text-slate-700 rounded-lg transition-colors disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </button>

        {/* Progress dots */}
        <div className="flex gap-2">
          {flashcards.map((_, index) => (
            <button
              key={index}
              onClick={() => {
                setCurrentIndex(index)
                setIsFlipped(false)
              }}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentIndex ? "bg-blue-600" : "bg-slate-300 hover:bg-slate-400"
              }`}
            />
          ))}
        </div>

        <button
          onClick={nextCard}
          disabled={flashcards.length <= 1}
          className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 disabled:bg-slate-50 disabled:text-slate-400 text-slate-700 rounded-lg transition-colors disabled:cursor-not-allowed"
        >
          Next
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Study tip */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Study Tip:</strong> Try to answer the question before flipping the card. This active recall technique
          helps improve memory retention.
        </p>
      </div>
    </div>
  )
}
