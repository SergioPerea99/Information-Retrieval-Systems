# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:09:30 2021

@author: Sergio Perea
"""
from stopper import Stopper
from filtrado import Filtrado
from stemmer import Stemmer

class Buscador(object):
    
    #Constructor por defecto
    def __init__(self, config, fich_consultas, doc_max):
        self.config = config
        self.fich_consultas = fich_consultas
        self.doc_max = doc_max
        filtro = Filtrado(fich_consultas)
        ruta_destino = config['DEFAULT']['ruta_fich_consultas_modificadas']
        
        #Hace la parte de normalización
        palabras_normalizadas = filtro.normalizacion_tokenizacion(ruta_destino)
        archivo = open(ruta_destino,"w")
        i = 0
        while i < len(palabras_normalizadas[1]):
            archivo.write(palabras_normalizadas[1][i])
            if i < len(palabras_normalizadas[1])-1:
                archivo.write("\n")
            i += 1
        archivo.close()
        
        #Hace la parte de stopper
        lista_stopword = config['DEFAULT']['ruta_lista_stopword']
        vacias = Stopper(lista_stopword) #Crear el stopper
        vacias.eliminacion_vacias(ruta_destino,ruta_destino) #Eliminar palabra vacía
    
        #Hace la parte de stemmer
        raices = Stemmer()
        self.lista_palabras_consulta = raices.extraccion_raices(ruta_destino, ruta_destino)
        