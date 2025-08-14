"use client"

import type React from "react"
import { AlertCircle, X } from "lucide-react"

interface ErrorMessageProps {
  message: string
  onDismiss: () => void
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss }) => {
  return (
    <div className="max-w-2xl mx-auto mb-6">
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-sm font-medium text-red-800 mb-1">Error generating flashcards</h3>
          <p className="text-sm text-red-700">{message}</p>
        </div>
        <button onClick={onDismiss} className="text-red-400 hover:text-red-600 transition-colors">
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
