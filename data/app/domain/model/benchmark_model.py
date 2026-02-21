from typing import Optional
from sqlmodel import Field, SQLModel

class Benchmark(SQLModel, table=True):
    __tablename__ = "benchmark"
    id : Optional[int] = Field(default=None, primary_key=True)
    temps: float = Field(default=0)
    is_numba: bool = Field(default=False)
    order : int = Field()
    image_id: int = Field(foreign_key="image.id", ondelete="CASCADE")