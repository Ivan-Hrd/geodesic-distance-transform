from pydantic import BaseModel

class TraitementRequest(BaseModel):
    img_path: str
    mask_path: str
    numba: bool | None = None