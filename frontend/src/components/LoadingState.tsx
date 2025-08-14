import type React from "react"
import { Sparkles, BookOpen } from "lucide-react"

export const LoadingState: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto text-center py-16">
      <div className="relative mb-8">
        {/* Animated book icon */}
        <div className="inline-block p-6 bg-blue-100 rounded-full animate-pulse">
          <BookOpen className="w-12 h-12 text-blue-600" />
        </div>

        {/* Floating sparkles */}
        <div className="absolute -top-2 -right-2 animate-bounce">
          <Sparkles className="w-6 h-6 text-yellow-500" />
        </div>
        <div className="absolute -bottom-2 -left-2 animate-bounce delay-300">
          <Sparkles className="w-4 h-4 text-blue-500" />
        </div>
      </div>

      <h2 className="text-2xl font-bold text-slate-800 mb-4 font-serif">Creating Your Flashcards</h2>
      <p className="text-slate-600 mb-8">Our AI is analyzing your content and crafting personalized study cards...</p>

      {/* Progress bar */}
      <div className="w-full bg-slate-200 rounded-full h-2 mb-4">
        <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: "70%" }}></div>
      </div>

      <p className="text-sm text-slate-500">This usually takes 10-30 seconds</p>
    </div>
  )
}
