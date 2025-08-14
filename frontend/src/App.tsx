"use client"

import { useState } from "react"
import { Header } from "./components/Header"
import { TextInput } from "./components/TextInput"
import { FlashcardDisplay } from "./components/FlashcardDisplay"
import { LoadingState } from "./components/LoadingState"
import { ErrorMessage } from "./components/ErrorMessage"
import type { Flashcard } from "./types"

function App() {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasGenerated, setHasGenerated] = useState(false)

  const handleGenerateFlashcards = async (text: string) => {
    setIsLoading(true)
    setError(null)

    try {
      // For demo purposes, create mock flashcards since we can't connect to the actual backend
      const mockFlashcards: Flashcard[] = [
        {
          question: "What is the main topic of this content?",
          answer:
            "The content discusses key concepts and important information that can be studied through flashcards.",
        },
        {
          question: "How can flashcards improve learning?",
          answer:
            "Flashcards use active recall and spaced repetition to help strengthen memory and improve retention of information.",
        },
        {
          question: "What makes AI-generated flashcards effective?",
          answer:
            "AI can analyze content to identify key concepts, create varied question types, and ensure comprehensive coverage of the material.",
        },
      ]

      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      setFlashcards(mockFlashcards)
      setHasGenerated(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate flashcards")
      setFlashcards([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setFlashcards([])
    setHasGenerated(false)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {!hasGenerated && !isLoading && (
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-slate-800 mb-4 font-serif">Transform Your Learning Experience</h1>
            <p className="text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
              Create AI-Powered Study Cards Effortlessly. Upload your text and let our AI craft the perfect study cards.
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
              <p className="text-sm text-blue-800">
                <strong>Demo Mode:</strong> This is a demonstration of the flashcard interface. In the full application,
                your text would be processed by OpenAI to generate personalized flashcards.
              </p>
            </div>
          </div>
        )}

        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {isLoading && <LoadingState />}

        {!hasGenerated && !isLoading && <TextInput onSubmit={handleGenerateFlashcards} />}

        {hasGenerated && !isLoading && flashcards.length > 0 && (
          <FlashcardDisplay flashcards={flashcards} onReset={handleReset} />
        )}
      </main>
    </div>
  )
}

export default App
