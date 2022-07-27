from flask import (
    Blueprint,render_template,request,session,redirect,url_for,current_app
)
from . import generarAbs as gAbs
from . import cosenoVectorial as cosV
from . import nlp 
from . import tdIdf as tdf
from . import jaccard
from werkzeug.utils import redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

bp = Blueprint('proyecto',__name__,url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('paginas/index.html')

@bp.route('/tabla', methods=['GET'])
def tabla():
    resultados = gAbs.leerXLSX('resultados.xlsx')
    tabla = list(zip(resultados['titulos'].tolist(),resultados['jaccard'].tolist(),resultados['cosenoVectorial'].tolist()))
    return render_template('paginas/tabla.html',tabla = tabla)


@bp.route('/formulario', methods=['GET','POST'])
def formulario():
    if request.method == 'POST':        
        titulo = request.form.get('tituloAbs')
        abstract = request.form.get('absOrg')
        session['titulo']=titulo
        session['abst']=abstract
        return redirect(url_for('proyecto.abstract'))
    return render_template('paginas/formulario.html')


@bp.route('/abstract', methods=['GET'])
def abstract():    
    titulo = session['titulo']
    abst= session['abst']
    numT= gAbs.obtenerNumTokens(abst) + gAbs.obtenerNumTokens(titulo)
    numT = int(numT*1.85)*100//75
    res = gAbs.generarAbs(titulo,numT)

    # #Calculo de Metricas    
    col = [abst,res.choices[0].text]
    _jaccard,_cosVectorial = calculoMetricas(col)
    return render_template('paginas/abs.html', similitud={'jaccard':_jaccard,'cosenoV':_cosVectorial}, 
    tituloAbst={'titulo':titulo},abst={'abst':abst},absG={'absg':res.choices[0].text}, tokens = {'real':len(abst.split()),'generado':len(res.choices[0].text.split())})



def calculoMetricas (col):
    colLim = nlp.limpiarDocumento(col,'es')
    #Metrica Jaccard
    jacValue = jaccard.jaccard(colLim[0],colLim[1])

    #Metrica Coseno Vectorial
    colLim = nlp.unirTokens(colLim)
    tfidf = TfidfVectorizer().fit_transform(colLim)
    cosV = cosine_similarity(tfidf[0:1],tfidf[1:2]).flatten()
    return jacValue,round(cosV[0],7)