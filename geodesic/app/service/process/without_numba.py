import numpy as np
import heapq


class PQueue:
    def __init__(self):
        self.heap = []

    def push(self, p: float, v):
        if isinstance(v, np.ndarray):
            v = tuple(v)
        heapq.heappush(self.heap, (p, v))

    def pop(self):
        if self.heap:
            p, v = heapq.heappop(self.heap)
            return p, v
        return None

    def empty(self):
        return len(self.heap) == 0


def setstatut(d,heap,img,status,y2,x2,y1,x1):
    if status[y2,x2] != "fait":
        dnew = d[y1,x1]  + abs(float(img[y1,x1]) - float(img[y2,x2]))
        if dnew < d[y2,x2]:
            d[y2,x2] = dnew
            heap.push(dnew,(y2,x2))

def geodesic_distance_without_numba(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    d = np.full(shape=img.shape,fill_value=1e10)
    status = np.full(shape=img.shape,fill_value="non_fait")
    d[mask > 0] = 0
    heap = PQueue()
    for i in np.argwhere(mask):
        status[i[0],i[1]] = "fait"
        heap.push(0,i)
    while not heap.empty():
        p = heap.pop()
        coord = p[1]
        coord_y = coord[0]
        coord_x = coord[1]
        status[coord_y,coord_x] = "fait"
        imin = max(coord_y - 1,0)
        imax = min(coord_y + 1,d.shape[0] - 1)
        jmin = max(coord_x - 1 , 0)
        jmax  = min(coord_x + 1, d.shape[1] - 1)
        setstatut(d,heap,img,status,imin,jmin,coord_y,coord_x)
        setstatut(d,heap,img,status,imin,coord_x,coord_y,coord_x)
        setstatut(d,heap,img,status,imin,jmax,coord_y,coord_x)
        setstatut(d,heap,img,status,coord_y,jmin,coord_y,coord_x)
        setstatut(d,heap,img,status,coord_y,jmax,coord_y,coord_x)
        setstatut(d,heap,img,status,imax,jmin,coord_y,coord_x)
        setstatut(d,heap,img,status,imax,coord_x,coord_y,coord_x)
        setstatut(d,heap,img,status,imax,jmax,coord_y,coord_x)
    return d
