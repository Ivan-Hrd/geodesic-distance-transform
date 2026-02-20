from sqlmodel import create_engine, SQLModel
from ..domain import Image,Benchmark

link = "postgresql://postgres:postgres@localhost:5432/imagedb"
engine = create_engine(link)

def data_base_init():
    return SQLModel.metadata.create_all(engine)