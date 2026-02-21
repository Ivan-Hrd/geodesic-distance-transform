from sqlmodel import Session, select
from ..model import *
from .image_repository import *






def db_create_benchmark(engine,img:str,isnumba:bool,temps:float):
    with Session(engine) as session: 
        image : Image = select_image(engine=engine,img=img)
        orders = 1
        if image is None:
            image : Image= create_image(engine=engine,img=img)
        else:
            for benchmark  in select_benchmark_from_image(engine=engine,img=img,with_numba=isnumba,number=None):
                orders = max(orders,benchmark.order)
            orders += 1
        print("order = ",orders)
        benchmark = Benchmark(temps=temps,is_numba=isnumba,order=orders,image_id=image.id)
        print("order = ",benchmark.order)
        session.add(benchmark)
        session.commit()
        session.refresh(benchmark)
        session.close()
        print("order = ",benchmark.order)
        return benchmark


def select_benchmark_from_image(engine, img:str,with_numba:bool,number: int):
    with Session(engine) as session:
        image : Image = select_image(engine=engine,img=img)
        if image is None:
            return []
                
        statement = select(Benchmark).where(Benchmark.image_id == image.id).where(Benchmark.is_numba == with_numba).order_by(Benchmark.order)
        if (number is not None or number == -1):
            statement = select(Benchmark).where(Benchmark.image_id == image.id).where(Benchmark.is_numba == with_numba).order_by(Benchmark.order).limit(number)        
        results = session.exec(statement).all()
        return results

def add_benchmark_multiple(engine,img:str,temps_list:list[float],isnumba:bool):
    with Session(engine) as session:
        image : Image = select_image(engine=engine,img=img)
        orders = 1
        if image is None:
            image : Image= create_image(engine=engine,img=img)
        else:
            for benchmark  in select_benchmark_from_image(engine=engine,img=img,with_numba=isnumba,number=None):
                orders = max(orders,benchmark.order)
            orders += 1
        benchmark_to_add = []
        for temp in temps_list:
            benchmark_to_add.append(Benchmark(temps=temp,is_numba=isnumba,order=orders,image_id=image.id))
            orders += 1
        session.add_all(benchmark_to_add)
        session.commit()
