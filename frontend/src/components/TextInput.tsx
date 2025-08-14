"use client"

import type React from "react"
import { useState, useRef } from "react"
import { Upload, FileText, Sparkles } from "lucide-react"

interface TextInputProps {
  onSubmit: (text: string) => void
}

export const TextInput: React.FC<TextInputProps> = ({ onSubmit }) => {
  const [text, setText] = useState("")
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim().length < 10) {
      alert("Please enter at least 10 characters of text")
      return
    }
    onSubmit(text.trim())
  }

  const handleFileUpload = (file: File) => {
    if (file.type === "text/plain") {
      const reader = new FileReader()
      reader.onload = (e) => {
        const content = e.target?.result as string
        setText(content)
      }
      reader.readAsText(file)
    } else {
      alert("Please upload a text file (.txt)")
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0])
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive ? "border-blue-400 bg-blue-50" : "border-slate-300 hover:border-slate-400"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-slate-700 mb-2">Upload a text file or paste content below</h3>
          <p className="text-slate-500 mb-4">Drag and drop a .txt file here, or click to browse</p>
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors"
          >
            <FileText className="w-4 h-4" />
            Choose File
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".txt"
            onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
            className="hidden"
          />
        </div>

        {/* Text Area */}
        <div>
          <label htmlFor="text-input" className="block text-sm font-medium text-slate-700 mb-2">
            Or paste your text content here
          </label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your lecture notes, article, or any educational content here..."
            className="w-full h-48 p-4 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            maxLength={10000}
          />
          <div className="flex justify-between items-center mt-2">
            <p className="text-sm text-slate-500">{text.length}/10,000 characters</p>
            <p className="text-sm text-slate-500">Minimum 10 characters required</p>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={text.trim().length < 10}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:hover:scale-100 flex items-center justify-center gap-3"
        >
          <Sparkles className="w-5 h-5" />
          Generate Flashcards
        </button>
      </form>
    </div>
  )
}
