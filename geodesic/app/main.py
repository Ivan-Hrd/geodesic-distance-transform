from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Local
from app.service import traitement


class TraitementRequest(BaseModel):
    img_path: str
    mask_path: str
    numba: bool | None = None

class TraitementResponse(BaseModel):
    traitement : list 

@app.get("/")
async def root():
    return {"message": "processing running"}

@app.post("/traitement", response_model=TraitementResponse)
async def read_item(traitements: TraitementRequest):
    return {"traitement": traitement.process_image(traitements.img_path,traitements.mask_path,traitements.numba)}