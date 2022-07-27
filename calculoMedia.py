import pandas as pd
import numpy as np

def leerXLSX(nombre_file):
    return pd.read_excel(nombre_file)

def exportarXLSX(nombre_file,modelos,jacm,cosVm):
    dic = {'modelo': modelos,'Jaccard Media': jacm,'Coseno Vectorial Media': cosVm,} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

dataset = ['resultados_curie_nicasop.xlsx','resultados_curie_san.xlsx','resultados_davinci_san.xlsx']
modelos = ['curie:ft-nicasop2-2022-07-26-18-50-18','curie:ft-personal-2022-07-26-02-11-01','davinci:ft-personal-2022-07-27-02-03-40 ']
mediaJ = []
mediaCV = []

for doc in dataset:
    datos = leerXLSX(doc)
    jaccard = datos['jaccard'].tolist()
    cosV = datos['cosenoVectorial'].tolist()
    mediaJ.append(np.mean(jaccard))
    mediaCV.append(np.mean(cosV))

exportarXLSX('media_similitud_por_modelo.xlsx',modelos,mediaJ,mediaCV)