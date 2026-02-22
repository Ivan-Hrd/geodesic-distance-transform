from sqlmodel import create_engine, SQLModel
from ..domain import Image,Benchmark
import os
link = os.getenv("DATABASE_URL","postgresql://postgres:postgres@localhost:5432/imagedb")
engine = create_engine(link)

def data_base_init():
    return SQLModel.metadata.create_all(engine)