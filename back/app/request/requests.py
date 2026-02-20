from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile

class TraitementRequest(BaseModel):
    img: UploadFile
    mask: UploadFile
    numba: bool | None = None

class TraitementRequestBench(BaseModel):
    img_path: str
    mask_path: str
    numba: bool | None = None
    n_iteration: int | None = 3