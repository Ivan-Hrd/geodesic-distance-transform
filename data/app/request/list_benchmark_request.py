from pydantic import BaseModel

class ListBenchmarkRequest(BaseModel):
    img: str
    time: list[float] | None
    isnumba: bool
    number : int | None