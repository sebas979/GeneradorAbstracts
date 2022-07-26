#### TF-IDF ####

## LIBRERIAS ##
import math
import numpy as np

def bagWords(dic,coleccion):
    bWords = np.zeros((len(dic['tokens']),len(coleccion)))
    for i in range (len(dic['tokens'])):
        ocurrencia = dic['ocurrencias'][i]
        for ocu in ocurrencia:
            bWords[i][ocu[0]-1] = ocu[1]
    return bWords

def pesadoTF(term):
    if term != 0:
        return 1 + math.log10(term)
    else:
        return 0

def documentF(matriz):
    doFrecuen = []
    for lista in matriz:
        doFrecuen.append(np.count_nonzero(lista))
    return doFrecuen

def matrizPTF(matriz):
    mPTF = np.zeros((len(matriz),len(matriz[0]))) 
    i = j = 0
    while True:
        mPTF[i][j] = pesadoTF(matriz[i][j])
        j += 1
        if j == len(matriz[0]):
            j = 0
            i += 1
        if i == len(matriz):
            break
    return mPTF

def IDF(df,N):
    idf = []
    for elemento in df:
        idf.append(math.log10(N/elemento))
    return idf

def TFIDF(wtf,idf):
    matriz = np.zeros((len(wtf),len(wtf[0])))
    i = j = 0
    while True:
        matriz[i][j] = wtf[i][j]*idf[i]
        j += 1
        if j == len(wtf[0]):
            j = 0
            i += 1
        if i == len(wtf):
            break
    return matriz