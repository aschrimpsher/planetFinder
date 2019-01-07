from math import sqrt

def euclidean_distance(x0, y0, x1, y1):
    result = sqrt((x0-x1)**2 + (y0-y1)**2)
    return result