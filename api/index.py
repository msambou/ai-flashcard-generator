import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app.main import app as fastapi_app

# ✅ Vercel needs the FastAPI app object to be called "app"
app = fastapi_app
