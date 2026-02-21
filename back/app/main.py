import json
from fastapi import FastAPI
import httpx
import requests
import os
import hashlib

# local
from app.response.response import *
from app.request.requests import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "backend running"}

geodesic_url = os.environ.get("GEODESIC_URL", "http://localhost:8000")
database_url = os.environ.get("DATABASE_URL", "http://localhost:8081")

def hash_image(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()

@app.post("/single_traitement", response_model=TraitementResponse)
async def single_traitement(img:UploadFile, msk:UploadFile, numba:bool):
    img_b = await img.read()
    msk_b = await msk.read()
    jsonObj = requests.post(f"{geodesic_url}/traitement?numba={numba}".lower(), files={"img": ("img.png", img_b, img.content_type), "msk": ("mask.png", msk_b, msk.content_type)})
    jsonObj = jsonObj.json()
    if jsonObj is not None:
        return jsonObj

@app.post("/benchmark", response_model=TraitementResponseBench)
async def bench(img:UploadFile, msk:UploadFile, numba:bool, n_iterations: int):
    img_b = await img.read()
    msk_b = await msk.read()
    # 1. is image in the database
    strHash = hash_image(img_b)
    response = requests.get(f"{database_url}/benchmarks/{strHash}/{n_iterations}/{numba}")
    json_obj = response.json()
    # 2. if yes gather it and return
    lstTimes = json_obj["time"]
    if lstTimes and len(lstTimes) > 0:
        nbToCompute = n_iterations - len(lstTimes)
        if nbToCompute <= 0:
            return {"benchResList": lstTimes}
        else:
            # get a benchmark of nbToCompute, add to db and concat it to lstTimes
            jsonObj = requests.post(f"{geodesic_url}/benchmark?numba={numba}&n_iterations={nbToCompute}".lower(), files={"img": ("img.png", img_b, img.content_type), "msk": ("mask.png", msk_b, msk.content_type)})
            jsonObj = jsonObj.json()
            newLstTime = jsonObj["benchResList"]
            requests.post(
            f"{database_url}/benchmarks_multi",
            json={
                "img": strHash,
                "time": newLstTime,
                "isnumba": numba,
                "number": -1
                }
            )
            # then return it
            return {"benchResList": lstTimes+newLstTime}
    # 3. else launch execution process on the endpoint and save into the db
    jsonObj = requests.post(f"{geodesic_url}/benchmark?numba={numba}&n_iterations={n_iterations}".lower(), files={"img": ("img.png", img_b, img.content_type), "msk": ("mask.png", msk_b, msk.content_type)})
    jsonObj = jsonObj.json()
    if jsonObj is not None:
        requests.post(
            f"{database_url}/benchmarks_multi",
            json={
                "img": strHash,
                "time": jsonObj["benchResList"],
                "isnumba": numba,
                "number": -1
            }
        )
        return jsonObj