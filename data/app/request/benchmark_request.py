
from pydantic import BaseModel

class BenchmarkRequest(BaseModel):
    img: str
    time: float
    isnumba: bool