from pydantic import BaseModel

class TraitementResponse(BaseModel):
    traitementList : str
    timeToExecute: float

class TraitementResponseBench(BaseModel):
    benchResList : list[float]