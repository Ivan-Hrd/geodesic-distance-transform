
from pydantic import BaseModel

class ListBenchmarkResponse(BaseModel):
    time: list[float]
    isnumba: bool