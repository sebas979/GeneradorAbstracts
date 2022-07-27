import web_scrapping as wsp

lexemas = wsp.leerXLSX('busqueda_finetuning.xlsx')['TAXONOMIA'].tolist()
wsp.obtenerDocumentos1(lexemas)
wsp.exportarXLSX('train2.xlsx')