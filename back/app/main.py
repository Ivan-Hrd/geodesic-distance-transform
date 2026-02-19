from fastapi import FastAPI
import httpx

# local
from app.response.response import *
from app.request.requests import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "backend running"}

@app.get("/single_traitement", response_model=TraitementResponse)
async def single_traitement():
    
    return {"img": [[0]],
            "exec_time": 0.0}