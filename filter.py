import numpy as np

def filter(Capacity_map):
    for x in range(1,np.shape(Capacity_map)[0]-1):
        for y in range(1,np.shape(Capacity_map)[0]-1):
            if Capacity_map[x,y] < 4:
                data = [Capacity_map[x-1,y], Capacity_map[x,y-1], Capacity_map[x+1,y], Capacity_map[x,y+1]]
                if min(data) > Capacity_map[x,y]:
                    Capacity_map[x, y] = min(data)
    return Capacity_map