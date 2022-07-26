from flask import current_app
import openai

def generarAbs(titulo, num):    
    openai.api_key = current_app.config['OPENAI_KEY']
    response = openai.Completion.create(
        model="ada:ft-personal-2022-07-25-05-21-29",
        prompt=titulo,
        temperature=0,
        max_tokens= num,
        top_p=1
    )
    return response

def obtenerNumTokens(text):
    return len(text.split())
    