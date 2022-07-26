##librerias
import re
from operator import index
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
# import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
# nltk.download('stopwords')

##funciones
def limpiarDocumento (cole,idioma):    
    colecciontok=[]
    for documento in cole:
        documentoaux = documento.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        documentoaux = re.sub('[^A-Za-z0-9]+',' ', documentoaux)#eliminar caracteres especiales  
        documentoaux = documentoaux.split()# tokenización
        documentoaux = quitarStopwords(idioma,documentoaux)# quitar stopwords
        documentoaux = stemming(documentoaux)# stemming
        colecciontok.append(documentoaux)
    return colecciontok

def quitarStopwords(tipo,documento):
    documentoLimpio = []
    if tipo == 'en':
        n = stopwords.words("english")
    elif tipo == 'es':
        n = stopwords.words("spanish")
    for token in documento:
        if token not in n:
            documentoLimpio.append(token)
    return documentoLimpio

def stemming(documento):
    stemmer = PorterStemmer()
    documentoS = []
    for token in documento:
        documentoS.append(stemmer.stem(token))
    return documentoS

def unirTokens(col):
    docUni = []
    for documento in col:
        doc = ' '.join(documento)
        docUni.append(doc)
    return docUni

def indexacionToken(coleccion):
    palabras=[]    
    for documento in coleccion:
        for token in documento:
            if token not in palabras:
                palabras.append(token)
    return palabras

def obtenPos(tok,lista):
    vpos=[]
    for pos in range (len(lista)):
        if tok == lista[pos]:
            vpos.append(pos+1)
    return vpos

def tokenDoc(tok,colDoc):
    vaux=[]
    for doc in range (len(colDoc)):
        vaux1=[]
        if tok in colDoc[doc]:
            vaux1.append(doc+1)
            posiciones = obtenPos(tok,colDoc[doc])
            vaux1.append(len(posiciones))
            vaux1.append(posiciones)
            vaux.append(vaux1)
    return vaux

def ocurrencias (dic,colDoc):
    vec=[]
    for token in dic:
        vec.append(tokenDoc(token,colDoc))
    return vec

def recuperarDatosHTML(enlace,etiqueta):
    file = urlopen(enlace)
    html = file.read()
    # file.close() #solo si la pagina web es dinamica
    soup = BeautifulSoup(html,features='html.parser')
    tit = []
    for p in soup.find_all(etiqueta):
        tit.append(p.get_text())
    return tit

def imprimirFII(vecT,vecO):
    print('Full Inverted Index')
    for j in range (len(vecT)):
        print(vecT[j],'-->',vecO[j])