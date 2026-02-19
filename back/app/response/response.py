from pydantic import BaseModel

class TraitementResponse(BaseModel):
    traitementList : list[list[float]]
    timeToExecute: float

class TraitementResponseBench(BaseModel):
    benchResList : list[float]