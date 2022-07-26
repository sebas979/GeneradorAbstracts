import numpy as np

def matrizNormal(matriz):
    matrizTran = np.transpose(matriz)
    matrizNormal = []
    for vector in matrizTran:
        modulo = np.linalg.norm(vector)
        matrizNormal.append(vector/modulo)
    return matrizNormal

def matrizDistacias(transpuesta):
    matrizD = np.zeros((len(transpuesta),len(transpuesta)))
    i = j = 0
    while True:
        if matrizD[i][j] == 0:
            matrizD[i][j] = matrizD[j][i] = round(np.dot(transpuesta[i],transpuesta[j]),2)
        j += 1
        if j == len(transpuesta):
            j = 0
            i += 1
        if i == len(transpuesta):
            break
    return matrizD

def matrizDistanciaPonderada(matriz1,matriz2,matriz3,ponderacines):
    matrizDistancias = np.zeros((len(matriz1),len(matriz1)))
    i = j = 0
    while True:
        matrizDistancias[i][j] = matriz1[i][j]*ponderacines[0] + matriz2[i][j]*ponderacines[1] + matriz3[i][j]*ponderacines[2]
        j += 1
        if j ==  len(matriz1):
            j = 0
            i += 1
        if i == len(matriz1):
            break
    return matrizDistancias