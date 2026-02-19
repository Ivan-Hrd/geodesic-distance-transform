import numba
import numpy as np
from numba import njit

heap_type = np.dtype([
    ('x',np.int64),
    ('y',np.int64)
])


TurpleArgument = numba.types.Tuple([numba.types.int64,numba.types.int64])
ValueList = numba.types.ListType(TurpleArgument)
Float = numba.types.float64


@njit
def push(values: dict, p, v):
        if  (p in values):
            values[p].append(v)
        else:
            tuple = (v[0],v[1])
            list_to_add = [tuple]
            values[p] = numba.typed.typedlist.List(list_to_add)


@njit
def pop(values):
        if empty(values):
            return None
        else:
            key = -1
            for p in values:
                if key == -1 or p < key:
                    key = p
            info = values[key]
            response = (key,info.pop(0))
            if (len(info) == 0):              
                values.pop(key)
            return response


@njit
def empty(values):
        return len(values) == 0
@njit
def setstatut_njit(d,heap,img,status,y2,x2,y1,x1):
    if status[y2,x2] != "fait":
        dnew = d[y1,x1]  + abs(float(img[y1,x1]) - float(img[y2,x2]))
        if dnew < d[y2,x2]:
            d[y2,x2] = dnew
            push(heap,dnew,(y2,x2))

        
@njit
def geodesic_distance_with_numba( img: np.ndarray, mask: np.ndarray) -> np.ndarray:

    heap = numba.typed.typeddict.Dict.empty(Float,ValueList)
    d = np.full(shape=img.shape,fill_value=1e10)
    status = np.full(shape=img.shape,fill_value="non_fait")
    
    len_y = mask.shape[0]
    len_x = mask.shape[1]
    for  i in range(len_y):
        for j in range(len_x):
            if (mask[i,j] > 0):
                d[i,j] = 0
                status[i,j] = "fait"
                push(heap,0,(i,j))
    while not empty(heap):
        p = pop(heap)
        priority, coordonnees = p
        coord_y, coord_x = coordonnees
        status[coord_y,coord_x] = "fait"
        imin = max(coord_y - 1,0)
        imax = min(coord_y + 1,d.shape[0] - 1)
        jmin = max(coord_x - 1 , 0)
        jmax  = min(coord_x + 1, d.shape[1] - 1)
        setstatut_njit(d,heap,img,status,imin,jmin,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,imin,coord_x,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,imin,jmax,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,coord_y,jmin,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,coord_y,jmax,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,imax,jmin,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,imax,coord_x,coord_y,coord_x)
        setstatut_njit(d,heap,img,status,imax,jmax,coord_y,coord_x)
    
    return d
