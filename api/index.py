import sys
import os
from fastapi import FastAPI
from backend.app.main import app as fastapi_app

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Wrap your app so root_path is /
app = FastAPI(root_path="")

# Mount the actual app
app.mount("/", fastapi_app)

# For Vercel
handler = app
