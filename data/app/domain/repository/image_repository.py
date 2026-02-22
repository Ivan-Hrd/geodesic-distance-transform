from ..model import *
from sqlmodel import Session, select, delete

def create_image(engine, img:str,temps=None,temps_numba=None):
    with Session(engine) as session:
        image : Image = Image(image=img,elapsed_time=temps,elapsed_time_numba=temps_numba)
        session.add(image)
        session.commit()
        session.refresh(image)
        return image

def update_image(engine, img:str,temps=None,temps_numba=None):
    with Session(engine) as session:
        image : Image = select_image(engine=engine,img=img)
        if image is None:
            return create_image(engine=engine,img=img,temps=temps,temps_numba=temps_numba)
        else:   
            if temps is not None:
                image.elapsed_time = temps
            if temps_numba is not None:
                image.elapsed_time_numba = temps_numba
            session.add(image)
            session.commit()
            session.refresh(image)
            return image

def select_image(engine, img:str) -> Image:
    with Session(engine) as session:
        statement = select(Image).where(Image.image == img)        
        result = session.exec(statement).first()
        return result

def is_image_in_db(engine, img:str):
    with Session(engine) as session:
        statement = select(Image).where(Image.image == img)        
        result = session.exec(statement).first()
        return result is not None
    
def db_remove_all(engine):
    with Session(engine) as session:
        session.exec(delete(Image))
        session.commit()
