from pydantic import BaseModel

class BenchmarkResponse(BaseModel):
    time: float
    isnumba: bool
    order:int