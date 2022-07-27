import requests
from bs4 import BeautifulSoup
from threading import Thread, Barrier

documents = []
global count_thread
count_thread = 20
final = Barrier(count_thread)
""" 
    - False si hay resultado
    - True si no hay resultado 
"""
def isEmpty(soup):
    if soup.find('div',attrs={'class':'result'}):
        return False
    else:
        return True

"""
    - Obtener cantidad de resultados
"""
def getCount(soup):
    limit = 20
    count = int(soup.find('div',attrs={'class':'search-stats'}).strong.next_sibling.next_sibling.string.replace(',','')) 
    div = count//limit
    pag =  div+1 if count%limit != 0 else div
    return count,pag
    
"""
    - Hace peticion 
"""
def doRequest(url):
    try:
        do_request = requests.get(url, timeout=15)
        if do_request.ok:
            soup = BeautifulSoup(do_request.content,'html5lib')
            return True,soup
        else:
            return False,None
    except Exception as error:
            print(error)
            return False,None

"""
    - Obtener detalle documento
"""
def getDetailsDocument(trs):
    objDetailDocument = {}
    objTopics =[["title","título"],
                ["keywords","palabras clave","palabras claves","descriptores / subjects"],
                ["resumen","descripcion","abstract","resumen traducido","resumen / abstract"],
                ["autor","authors"],
                ["fecha de publicación"],
                ["isbn","issn"],
                ["editorial"]]

    limit = range(3)

    #Recorremos la tabla
    for tr in trs:
        td = tr.find_all('td')
        topic = td[0].string.lower().replace(':','').strip()
        detail = td[1].string if td[1].string else td[1].get_text(',') 

        for x,ot in enumerate(objTopics): 
            if topic in ot: #verificamos que los atributos se encuentren en nuestro vector,
                if (x in limit) and (not detail or 'the' in detail): #validamos que no haya null en nuestros atributos importantes "title, autor, resumen" ######
                    return None   
                objDetailDocument.setdefault(ot[0], detail) 
    
    #Filtro adicional
    #Valida que si se obtuvieron los parametros importantes que son "title, autor, resumen"
    for o in objTopics[:3]:
        if not o[0] in list(objDetailDocument.keys()):
            return None

    return objDetailDocument

"""
    - Obtener documentos
"""
def getDocument(url,name):
    bool,soup = doRequest(url)
    objDocument = {}
    if bool:
        table = soup.find('table',attrs={'class':'table itemDisplayTable'})
        if table: 
            trs = table.find_all('tr')
            details = getDetailsDocument(trs) 
            if not details:
                final.wait()
                return None
            objDocument.setdefault("name",name)
            objDocument.setdefault("url",url)
            objDocument.setdefault("info",details) 
            
            documents.append(objDocument) 
            final.wait()               
            return details
        else:
            final.wait()
            #print('No cumple con el formato establecido')
            return None
    else:
        final.wait()
        #print('Ha ocurrido un error en la peticion')
        return None
"""
    - Metodo de parada hilos de sobra
"""
def stopThread():
    final.wait()

"""
    - Obtener lista de documentos
"""
def getListDocument(soup):
    """
    documents = []
    for doc in soup.find_all('div',attrs={'class': 'result-fulltext'}):
        objDocument = getDocument(doc.a.get("href"))  
        if objDocument:
            documents.append({
                "name": doc.previous_sibling.previous_sibling.string.strip(),
                "url": doc.a.get("href"),
                "info": objDocument
            })
    return documents
    """
    thread = []
    for doc in soup.find_all('div',attrs={'class': 'result-fulltext'}):
        thread.append(Thread(target=(getDocument),args=(doc.a.get("href"),doc.previous_sibling.previous_sibling.string.strip())))
    #METODO PARA CUANDO LOS HILOS CREADOS SEAN MENORES QUE 20
    if len(thread)<count_thread:
        for i in range(count_thread-len(thread)):
            thread.append(Thread(target=stopThread))
    for i in thread:
        i.start()
    for i in thread:
        i.join()

"""
    - Funcion Principal
"""
def start(query):
    documents.clear()
    url = "https://rraae.cedia.edu.ec/Search/Results?lookfor[]={}&type=AllFields".format(query)
    bool,soup = doRequest(url)
    if bool:
        if isEmpty(soup):
            return {'msg': 'No hay resultados'}
        else:
            count,pag = getCount(soup)
            count_thread = 20 if count >= 20 else count
            
            #documents = []
            i = 1
            while i <= pag:        
                if len(documents) < 30:
                    print("pages: {} documents: {}".format(i,len(documents)) )
                    #documents += getListDocument(soup)
                    getListDocument(soup)
                    bool,soup = doRequest("{}&page={}".format(url,i+1))
                    i+=1
                    if not bool: break
                else:   
                    break
            return {"pag": pag,"count":len(documents), "documents": documents}
    else:
        return {"msg":'Ha ocurrido un error en la peticion'}