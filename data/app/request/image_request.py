
from pydantic import BaseModel

class ImageRequest(BaseModel):
    img: str
    numba_time : float | None
    time: float | None
