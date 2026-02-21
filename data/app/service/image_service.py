from ..domain import Image,image_repository
from .server_service import engine
from ..reponse import ImageResponse

def add_image(img: str,not_nb_time: float,nb_time:float):
    time = not_nb_time
    if not_nb_time == -1:
        time = None
    numba_time = nb_time
    if numba_time == -1:
        numba_time= None
    image : Image  = image_repository.create_image(engine=engine,img=img,temps=time,temps_numba=numba_time)
    return ImageResponse(img=image.image,numba_time=image.elapsed_time_numba,time=image.elapsed_time)

def get_image(image:str):
    image : Image =  image_repository.select_image(engine=engine,img=image)
    if image is None:
        return ImageResponse(img=None,numba_time=None,time=None)
    return ImageResponse(img=image.image,numba_time=image.elapsed_time_numba,time=image.elapsed_time)

def remove_all():
    image_repository.db_remove_all(engine=engine)