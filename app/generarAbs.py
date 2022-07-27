from flask import current_app
import openai
import pandas as pd

def generarAbs(titulo, num):    
    openai.api_key = current_app.config['OPENAI_KEY']
    response = openai.Completion.create(
        model="curie:ft-personal-2022-07-26-02-11-01",
        prompt=titulo,
        temperature=0.8,
        max_tokens= num,
        top_p=1
    )
    return response

def obtenerNumTokens(text):
    return len(text.split())


def exportarXLSX(nombre_file,tit,absR,absG):
    dic = {'titulos': tit,'AbstractR': absR,'AbstractG': absG,} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

def leerXLSX(nombre_file):
    return pd.read_excel(nombre_file)
    