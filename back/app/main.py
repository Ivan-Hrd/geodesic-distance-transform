import json
from fastapi import FastAPI
import httpx
import requests
import os

# local
from app.response.response import *
from app.request.requests import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "backend running"}

geodesic_url = os.environ.get("GEODESIC_URL", "http://localhost:8000")

@app.post("/single_traitement", response_model=TraitementResponse)
async def single_traitement(img:UploadFile, msk:UploadFile, numba:bool):
    # 1. is image in the database
    # 2. if yes gather it and return
    # 3. else launch execution process on the endpoint and save into the db
    img_b = await img.read()
    msk_b = await msk.read()
    jsonObj = requests.post(f"{geodesic_url}/traitement?numba={numba}".lower(), files={"img": ("img.png", img_b, img.content_type), "msk": ("mask.png", msk_b, msk.content_type)})
    jsonObj = jsonObj.json()
    if jsonObj is not None:
        return jsonObj

@app.post("/benchmark", response_model=TraitementResponseBench)
async def bench(img:UploadFile, msk:UploadFile, numba:bool, n_iterations: int):
    # 1. is image in the database
    # 2. if yes gather it and return
    # 3. else launch execution process on the endpoint and save into the db
    img_b = await img.read()
    msk_b = await msk.read()
    jsonObj = requests.post(f"{geodesic_url}/benchmark?numba={numba}&n_iterations={n_iterations}".lower(), files={"img": ("img.png", img_b, img.content_type), "msk": ("mask.png", msk_b, msk.content_type)})
    jsonObj = jsonObj.json()
    if jsonObj is not None:
        return jsonObj