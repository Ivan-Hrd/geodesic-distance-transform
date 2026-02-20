from pydantic import BaseModel

class TraitementResponse(BaseModel):
    traitementList : str
    shape: list[int]      
    timeToExecute: float

class TraitementResponseBench(BaseModel):
    benchResList : list[float]