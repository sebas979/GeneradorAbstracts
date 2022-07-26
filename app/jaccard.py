#### JACCARD ####

#### LIBRERIAS ####
import numpy as np

def jaccard(a,b):
    intersec = len(np.intersect1d(a,b))   
    uni = len(np.union1d(a,b)) 
    return round(intersec/uni,2)

def matrizJaccard(coleccion):
    matriz = np.zeros((len(coleccion),len(coleccion)))
    i = j = 0
    while True:
        if matriz[i][j] == 0:
            matriz[i][j] = matriz[j][i] = jaccard(coleccion[i],coleccion[j])
        j += 1
        if j == len(coleccion):
            j = 0 
            i += 1
        if i == len(coleccion):
            break
    return matriz