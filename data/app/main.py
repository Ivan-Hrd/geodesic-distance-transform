from fastapi import FastAPI
from contextlib import asynccontextmanager


# Local
from .service import image_service, benchmarck_service, server_service
from .request import *
from .reponse import *



@asynccontextmanager
async def lifespan(app:FastAPI):
    server_service.data_base_init() 
    yield

app = FastAPI(lifespan=lifespan)




@app.get("/")
async def root():
    return {"message": "processing running"}


@app.get("/image/{image}", response_model=ImageResponse)
def do_get_image(image: str):
    return image_service.get_image(image=image)

 
@app.post("/image", response_model=ImageResponse)
def  do_add_image(image_request: ImageRequest):
    return image_service.add_image(image_request.img,image_request.time,image_request.numba_time)



@app.delete("/image")
def  do_delete_image():
    image_service.remove_all()



@app.post("/benchmark", response_model=BenchmarkResponse)
def do_add_benchmark(benchmark: BenchmarkRequest):
    return benchmarck_service.add_benchmark(benchmark.img,benchmark.time,benchmark.isnumba)

@app.post("/benchmarks_multi")
def do_add_benchmarks(benchmark: ListBenchmarkRequest):
    benchmarck_service.add_benchmark_multi(benchmark.img,benchmark.time,benchmark.isnumba)


@app.get("/benchmarks/{image}/{number}/{numba}", response_model=ListBenchmarkResponse)
def do_get_benchmark(image:str,number:int,numba:bool):
    return benchmarck_service.get_benchmark(image,numba,number)
