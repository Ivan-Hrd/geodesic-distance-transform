from ..domain import benchmark_repository, Benchmark
from .server_service import engine
from ..reponse import BenchmarkResponse, ListBenchmarkResponse


def add_benchmark(img:str,temps:float,isnumba:bool):
    value : Benchmark = benchmark_repository.db_create_benchmark(engine=engine,img=img,isnumba=isnumba,temps=temps)
    return BenchmarkResponse(time=value.temps,isnumba=value.is_numba,order=value.order)

def add_benchmark_multi(img:str,temps:list[float],isnumba:bool):
    benchmark_repository.add_benchmark_multiple(engine=engine,img=img,temps_list=temps,isnumba=isnumba)

def get_benchmark(img:str,isnumba:bool,value : int):
    value: list[Benchmark] = benchmark_repository.select_benchmark_from_image(engine=engine,img=img,with_numba=isnumba,number=value)
    temps_list = [x.temps for x in value ]
    return ListBenchmarkResponse(time=temps_list,isnumba=isnumba) 