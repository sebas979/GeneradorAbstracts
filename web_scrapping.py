import requests
from bs4 import BeautifulSoup
from threading import Thread, Barrier
import pandas as pd

titulos = []
abstracts = []
objTopics = ["resumen","descripción","abstract","resumen traducido","resumen / abstract","description"]

objTopics1 =[["title","título","título "],
             ["resumen","resumen "]
]

def isEmpty(soup):
    if soup.find('div',attrs={'class':'result'}):
        return False
    else:
        return True

def doRequest(url,parse):
    try:
        do_request = requests.get(url, timeout=15)
        if do_request.ok:
            soup = BeautifulSoup(do_request.content,parse)
            return True,soup
        else:
            return False,None
    except Exception as error:
            print(error)
            return False,None
def leerXLSX(nombre_file):
    return pd.read_excel(nombre_file)

def exportarXLSX(nombre_file):
    dic = {'prompt': titulos,'completion': abstracts} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

def exportarXLSX1(nombre_file):
    dic = {'completion': abstracts} 
    df = pd.DataFrame(dic) 
    df.to_excel(nombre_file,index=False,encoding='utf-8')

##Primer web scraping
def obtenerDocumentos(lexemas):
    for lexema in lexemas:
        res_bool,soup = doRequest("https://rraae.cedia.edu.ec/Search/Results?limit=20&lookfor={}&type=AllFields&filter%5B%5D=language%3A%22spa%22".format(lexema.replace(' ','+')),'html5lib')
        if res_bool:
            docs = soup.find_all('div',attrs={'class': 'result-title'})
            for doc in docs:
                url = "https://rraae.cedia.edu.ec"+doc.a.get("href")
                res_bool,soup1 = doRequest(url)
                if res_bool:
                    contenido = soup1.find('div',attrs={'class':'media-body'})
                    if contenido:
                        titulo = contenido.find('h1').string
                        dls = contenido.find_all('dl')
                        for dl in dls:
                            topic = dl.find('dt').string.lower().strip()
                            if topic in objTopics:
                                detail = dl.find('dd').p.string if dl.find('dd').p.string else dl.find('dd').p.get_text()
                                if detail and ('--'!=detail):
                                    titulos.append(titulo)
                                    abstracts.append(detail.strip())
                                break

##Segundo web scraping
def obtenerDocumentos1(lexemas):
    for lexema in lexemas:
        res_bool,soup = doRequest("https://rraae.cedia.edu.ec/Search/Results?limit=20&lookfor={}&type=AllFields&filter%5B%5D=language%3A%22spa%22".format(lexema.replace(' ','+')),'html5lib')
        if res_bool:
            docs = soup.find_all('div',attrs={'class': 'result-fulltext'})
            for doc in docs:
                url = doc.a.get("href")
                res_bool,soup1 = doRequest(url,'xml')
                if res_bool:
                    contenido = soup1.find('table',attrs={'class':'table itemDisplayTable'})
                    if contenido:
                        trs = contenido.find_all('tr')
                        tituloAUX = ""
                        for tr in trs:
                            td = tr.find_all('td')
                            topic = td[0].string.lower().replace(':','').strip()
                            detail = td[1].string if td[1].string else td[1].get_text(',') 
                            for x,ot in enumerate(objTopics1):
                                if topic in ot:
                                    if not detail or (not 'the' in detail):
                                        if topic in objTopics1[0]:
                                            tituloAUX = detail.strip()
                                        elif topic in objTopics1[1]:
                                            if detail != "":
                                                titulos.append(tituloAUX)
                                                abstracts.append(detail.strip())
                                        break