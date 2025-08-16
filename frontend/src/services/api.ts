import axios from "axios"
import type { FlashcardResponse } from "../types"


// Handle environment variable safely
const getApiUrl = () => {
  if (typeof window !== "undefined") {
    // Client-side
    // return (window as any).process?.env?.VITE_API_URL || "http://localhost:8000"
    return import.meta.env.VITE_API_URL || "http://localhost:8000"
  }
  // Server-side or fallback
  return "http://localhost:8000"
}

const API_BASE_URL = getApiUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
})

api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    console.error("Request error:", error)
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (response) => {
    console.log(`Response received:`, response.status)
    return response
  },
  (error) => {
    console.error("Response error:", error.response?.data || error.message)
    return Promise.reject(error)
  },
)

export const generateFlashcards = async (text: string): Promise<FlashcardResponse> => {
  try {
    const response = await api.post<FlashcardResponse>("/generate-flashcards", {
      text: text.trim(),
    })
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || "Failed to generate flashcards"
      throw new Error(message)
    }
    throw new Error("Network error occurred")
  }
}

export const healthCheck = async (): Promise<{ status: string; openai_configured?: boolean }> => {
  const response = await api.get("/health")
  return response.data
}
