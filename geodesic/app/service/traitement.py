from imageio.v3 import imread
import app.service.process.without_numba
import app.service.process.with_numba

def process_image(img_path,mask_path,is_numba):
    resp = None
    img, mask = load_pictures(img_path, mask_path)
    if is_numba:
        # call traitement_numba
        return  traitement_numba(img, mask).tolist()
    else:
        # call traitement
        return  traitement(img, mask).tolist()


def load_pictures(img_path, mask_path):
    img = imread(img_path)
    mask = imread(mask_path)
    return img, mask



def traitement(img, mask):
    # Traitement de l'image et du masque sans numba
    return without_numba.geodesic_distance_without_numba(img,mask)

def traitement_numba(img, mask):
    # Traitement de l'image et du masque avec numba
    return with_numba.geodesic_distance_with_numba(img,mask)