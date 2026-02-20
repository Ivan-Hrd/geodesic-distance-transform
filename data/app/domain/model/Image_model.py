from typing import Optional
from sqlmodel import Field, SQLModel

class Image(SQLModel, table=True):
    __tablename__ = "image"
    id : Optional[int] = Field(default=None, primary_key=True)
    image: str = Field(index=True)
    elapsed_time:Optional[float] = Field(default=None)
    elapsed_time_numba:Optional[float] = Field(default=None)