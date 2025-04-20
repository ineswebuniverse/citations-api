
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from pydantic import BaseModel
import uvicorn
from typing import Optional
from fastapi.responses import JSONResponse

# Pour le local uniquement : charge le .env
from dotenv import load_dotenv
load_dotenv()  # lit le .env et injecte dans os.environ

# Récupération de la clé
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise RuntimeError("Missing HF_API_KEY in environment")

app = FastAPI()

# Autoriser les requêtes depuis ton domaine
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://citations-bank.mon-ebbok-pdf.site",  # your front‑end
        "http://localhost:8000",                      # for local tests
        "https://citations-api.onrender.com"          # if you call from itself
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Définir la structure de la requête
#class NicheRequest(BaseModel):
    #niche: str
    
client = InferenceClient(api_key=HF_API_KEY)

@app.get("/authors")
def get_authors(niche: str = ""):
    try:
        if not niche:
            return JSONResponse(status_code=400, content={"error": "Niche is required"})

        # Simule une base de données d'auteurs par niche (à adapter)
        authors_by_niche = {
            "Marketing": ["Seth Godin", "Simon Sinek", "Philip Kotler"],
            "Développement personnel": ["Tony Robbins", "Brené Brown", "Robin Sharma"],
            "Entrepreneuriat": ["Elon Musk", "Gary Vaynerchuk", "Peter Thiel"]
        }

        authors = authors_by_niche.get(niche, [])
        return {"authors": authors}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

#Resoudre Erreur : 127.0.0.1:46476 - "HEAD / HTTP/1.1" 404 Not Found
@app.get("/")
def root():
    return {"message": "Citation API is running."}

