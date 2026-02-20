from imageio.v3 import imread
import time
from .process import *
from matplotlib import pyplot as plt
import numpy as np
import base64
# local

def process_image(img,mask,is_numba):
    if is_numba:
        # setup timer
        start = time.perf_counter()
        # call traitement_numba
        lst = _traitement_numba(img, mask)
        elapsed = time.perf_counter() - start
        return  base64.b64encode(lst.tobytes()).decode('utf-8'), lst.shape, elapsed
    else:
        # setup timer
        start = time.perf_counter()
        # call traitement_numba
        lst = _traitement(img, mask)
        elapsed = time.perf_counter() - start
        return  base64.b64encode(lst.tobytes()).decode('utf-8'), lst.shape, elapsed

def process_benchmark(img,mask,is_numba, n):
    lstBench = []
    if is_numba:
        for i in range(n):
            # setup timer
            start = time.perf_counter()
            # call traitement_numba
            _ = _traitement_numba(img, mask)
            elapsed = time.perf_counter() - start
            lstBench.append(elapsed)
    else:
        for i in range(n):
            # setup timer
            start = time.perf_counter()
            # call traitement
            _ = _traitement(img, mask)
            elapsed = time.perf_counter() - start
            lstBench.append(elapsed)
    return lstBench


def _load_pictures(img_path, mask_path):
    img = imread(img_path)
    mask = imread(mask_path)
    return img, mask



def _traitement(img, mask):
    # Traitement de l'image et du masque sans numba
    return distance_without_numba(img,mask)

def _traitement_numba(img, mask):
    # Traitement de l'image et du masque avec numba
    return distance_numba(img,mask)