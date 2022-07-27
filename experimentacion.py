from operator import length_hint
from pyexpat import model
from click import prompt
import openai
import os
from dotenv import load_dotenv
import pandas as pd

""" 
LLAVES UTILIZADOS PARA EL ENTRENAMIENTO DE LOS MODELOS 
OPENAI_API_KEYS=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
OPENAI_API_KEYS1=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
OPENAI_API_KEYN=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
"""

load_dotenv()

def exportarXLSX(nombre_file,tit,absR,absG):
    dic = {'titulos': tit,'AbstractR': absR,'AbstractG': absG,} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

def leerXLSX(nombre_file):
    return pd.read_excel(nombre_file)

openai.api_key = os.getenv("OPENAI_API_KEYS1")

datos_experimentos = leerXLSX("prueba.xlsx")
titulos = datos_experimentos['titulo'].tolist()
abstractsR = datos_experimentos['resumen'].tolist()
abstractsG = []


for x,tit in enumerate(titulos):
    numT = len(abstractsR[x].split()) + len(tit.split())
    tok = int(numT*1.85)*100//75
    print(tok)
    response = openai.Completion.create(
        model="davinci:ft-personal-2022-07-27-02-03-40",
        prompt=tit,
        temperature=0.4,
        max_tokens= tok,
        top_p=1
    )
    abstractsG.append(response.choices[0].text)
exportarXLSX('dataset_davinci_san.xlsx',titulos,abstractsR,abstractsG)