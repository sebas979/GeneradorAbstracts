from flask import (
    Blueprint,render_template,request,session,redirect,url_for,current_app
)
from . import generarAbs as gAbs
from . import cosenoVectorial as cosV
from . import nlp 
from . import tdIdf as tdf
from . import jaccard
from werkzeug.utils import redirect
from werkzeug.wrappers import response
import pandas as pd
import numpy as np
"""import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
import io
import seaborn as sns
from sklearn.manifold import MDS
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering"""



bp = Blueprint('proyecto',__name__,url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('paginas/index.html')

@bp.route('/tabla', methods=['GET'])
def tabla():
    return render_template('paginas/tabla.html')


@bp.route('/formulario', methods=['GET','POST'])
def formulario():
#    datosfiltrados = datos
    if request.method == 'POST':        
        titulo = request.form.get('tituloAbs')
        abstract = request.form.get('absOrg')
        session['titulo']=titulo
        session['abst']=abstract
        return redirect(url_for('proyecto.abstract'))
        #print(titulo,abstrac)    


    return render_template('paginas/formulario.html')


@bp.route('/abstract', methods=['GET'])
def abstract():    
    titulo = session['titulo']
    abst= session['abst']
    numT= gAbs.obtenerNumTokens(abst)
    res = gAbs.generarAbs(titulo,numT)

    #Calculo de Metricas    
    col = [abst,res.choices[0].text]
    _jaccard,_cosVectorial = calculoMetricas(col)
#    datosfiltrados = datos
    return render_template('paginas/abs.html', similitud={'jaccard':_jaccard,'cosenoV':_cosVectorial}, 
    tituloAbst={'titulo':titulo},abst={'abst':abst},absG={'absg':res.choices[0].text})



def calculoMetricas (col):
    colLim = nlp.limpiarDocumento(col,'es')
    #Metrica Jaccard
    jacValue = jaccard.jaccard(colLim[0],colLim[1])

    #Metrica Coseno Vectorial
    diccionario={'tokens':[],'ocurrencias':[]}
    diccionario['tokens']= nlp.indexacionToken(colLim)
    diccionario['ocurrencias'] = nlp.ocurrencias(diccionario['tokens'],colLim)
    #TF-IDF
    matriz = tdf.bagWords(diccionario,colLim)
    wtf = tdf.matrizPTF(matriz)
    dF = tdf.documentF(wtf)
    idf = tdf.IDF(dF,len(colLim))
    tf_idf = tdf.TFIDF(wtf,idf)
    #Coseno Vectorial
    matrizN = cosV.matrizNormal(tf_idf)
    matrizAbs = cosV.matrizDistacias(matrizN)
    return jacValue,matrizAbs[0][1]


""" @bp.route('/test', methods=['GET','POST'])
def matriz():
    datosfiltrados = datos
    if request.method == 'POST':
        filtro = ''
        tipo = request.form.get('tipo',type=int)
        tema = request.form.get('tema')
        if tipo != 2 or tema != 'todos':
            if tipo != 2:
                if tipo == 1:
                    filtro = 'tipo == 1'
                if tipo == 0:
                    filtro = 'tipo == 0'
                if tema != 'todos':
                    if tema == 'exactas':
                        filtro += 'and tema == "Ciencias exactas"'
                    if tema == 'medi':
                        filtro += 'and tema == "Medicina"'
                    if tema == 'sociales':
                        filtro += 'and tema == "Ciencias Sociales"'
                    if tema == 'compu':
                        filtro += 'and tema == "Computacion"'
            else:
                if tema == 'exactas':
                    filtro = 'tema == "Ciencias exactas"'
                if tema == 'medi':
                    filtro = 'tema == "Medicina"'
                if tema == 'sociales':
                    filtro = 'tema == "Ciencias Sociales"'
                if tema == 'compu':
                    filtro = 'tema == "Computacion"'
            datosfiltrados = datos.query(filtro)
    matriz = list(zip(datosfiltrados['titulo'].tolist(),datosfiltrados['keywords'].tolist(),datosfiltrados['abstract'].tolist()))
    return render_template('paginas/matriz.html',filas=len(matriz),matriz=matriz) """