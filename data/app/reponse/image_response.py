
from pydantic import BaseModel

class ImageResponse(BaseModel):
    img: str | None
    numba_time : float | None
    time: float | None