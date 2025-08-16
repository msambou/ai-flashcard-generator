import os
import json
import logging
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="AI Flashcard Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Flashcard Generator API", "status": "running"}


# ✅ Ensure Vercel can detect `app`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
