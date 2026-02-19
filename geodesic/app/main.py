from fastapi import FastAPI
import numpy as np
from PIL import Image
from io import BytesIO

app = FastAPI()

# Local
from .service import *
from app.request.requests import *
from app.response.response import *

def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))

@app.get("/")
async def root():
    return {"message": "processing running"}

@app.post("/traitement", response_model=TraitementResponse)
async def execute_single(img:UploadFile, msk:UploadFile, numba:bool):
    imgBase = await img.read()
    mskBase = await msk.read()
    image = load_image_into_numpy_array(imgBase)
    mask = load_image_into_numpy_array(mskBase)
    listTraitement, timeToExecute = process_image(image,mask,numba)
    return {"traitementList": listTraitement,
            "timeToExecute": timeToExecute}

@app.post("/benchmark", response_model=TraitementResponseBench)
def execute_bench(traitementRequest: TraitementRequestBench):
    listBench = process_benchmark(traitementRequest.img_path,traitementRequest.mask_path,traitementRequest.numba, traitementRequest.n_iteration)
    return {"benchResList": listBench}