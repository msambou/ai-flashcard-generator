import type React from "react"
import { BookOpen } from "lucide-react"

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-slate-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-lg">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800 font-serif">AI Flashcard Generator</h1>
            <p className="text-sm text-slate-600">Powered by artificial intelligence</p>
          </div>
        </div>
      </div>
    </header>
  )
}
