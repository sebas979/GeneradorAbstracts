import pandas as pd
import nlp
import jaccard
import tdIdf as tdf
import cosenoVectorial as cosV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

def leerXLSX(nombre_file):
    return pd.read_excel(nombre_file)

def exportarXLSX(nombre_file,tit,jac,cosV):
    dic = {'titulos': tit,'jaccard': jac,'cosenoVectorial': cosV,} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

def exportarXLSX1(nombre_file,modelo,tiempo):
    dic = {'modelo': modelo,'tiempo': tiempo} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

def calculoMetricas (col):
    colLim = nlp.limpiarDocumento(col,'es')

    #Metrica Jaccard
    jacValue = jaccard.jaccard(colLim[0],colLim[1])

    #Metrica Coseno Vectorial
    colLim = nlp.unirTokens(colLim)
    tfidf = TfidfVectorizer().fit_transform(colLim)
    cosV = cosine_similarity(tfidf[0:1],tfidf[1:2]).flatten()
    return jacValue,round(cosV[0],7)

datasets = ['dataset_curie_nicasop.xlsx','dataset_curie_san.xlsx','dataset_davinci_san.xlsx']
resultado = ['resultados_curie_nicasop.xlsx','resultados_curie_san.xlsx','resultados_davinci_san.xlsx']
modelos = ['curie:ft-nicasop2-2022-07-26-18-50-18','curie:ft-personal-2022-07-26-02-11-01','davinci:ft-personal-2022-07-27-02-03-40 ']
tiempos = []
for x,data in enumerate(datasets):
    start = time.process_time()
    datos = leerXLSX(data)
    tit = datos['titulos'].tolist()
    absR = datos['AbstractR'].tolist()
    absG = datos['AbstractG'].tolist()

    jaccardValues = []
    cosVectorialValues = []

    for y, abst in enumerate(absR):
        jac, cosVec = calculoMetricas([abst,absG[y]])
        jaccardValues.append(jac)
        cosVectorialValues.append(cosVec)
    exportarXLSX(resultado[x],tit,jaccardValues,cosVectorialValues)

    end = time.process_time()
    tiempos.append(end-start)
exportarXLSX1('tiempos de ejecución.xlsx',modelos,tiempos)