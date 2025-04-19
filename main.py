from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient

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

API_KEY = "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"  # Ton token Hugging Face
client = InferenceClient(api_key=API_KEY)

@app.post("/get-authors")
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
