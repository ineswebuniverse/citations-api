# Securiser la cle API
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient

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
    allow_origins=["*"],  # Pour tests, ensuite remplace par ["https://citations-bank.mon-ebbok-pdf.site"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définir la structure de la requête
class NicheRequest(BaseModel):
    niche: str
    
client = InferenceClient(api_key=HF_API_KEY)

@app.post("/authors")
async def get_authors(req: NicheRequest):
    prompt = f"""List 10 authors famous in the "{req.niche}" field for their quotes. 
- One name per line 
- No numbering
- No extra text"""
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        return {"authors": completion.choices[0].message.content.strip().split("\n")}
    except Exception as e:
        return {"error": str(e)}
