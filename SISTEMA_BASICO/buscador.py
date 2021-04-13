# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:09:30 2021

@author: Sergio Perea
"""
from stopper import Stopper
from filtrado import Filtrado
from stemmer import Stemmer
from palabra_frecuencia import Pares_Palabra_Frecuencia
from fich_norm import Ficheros_Pesos_Normalizados

class Buscador(object):
    
    #Constructor por defecto
    def __init__(self, config, fich_consultas, doc_max):
        self.config = config
        self.fich_consultas = fich_consultas
        self.doc_max = doc_max
        filtro = Filtrado(fich_consultas)
        ruta_destino = config['DEFAULT']['ruta_fich_consultas_modificadas']
        
        #Hace la parte de normalización
        filtro.normalizacion_tokenizacion(ruta_destino)
        
        #Hace la parte de stopper
        lista_stopword = config['DEFAULT']['ruta_lista_stopword']
        vacias = Stopper(lista_stopword) #Crear el stopper
        vacias.eliminacion_vacias(ruta_destino,ruta_destino) #Eliminar palabra vacía
    
        #Hace la parte de stemmer
        raices = Stemmer()
        lista_palabras_consulta = raices.extraccion_raices(ruta_destino, ruta_destino)
        lista_aux = []
        self.lista_consultas = []
        for i in lista_palabras_consulta[1]:
            if not i  == '':
                lista_aux.append(i)
            else:
                self.lista_consultas.append(lista_aux.copy())
                lista_aux.clear()
        
    
    def procesar_pesos(self):
        pares_palabra_frecuencia_online = Pares_Palabra_Frecuencia()
        fich_pesosNorm_online = Ficheros_Pesos_Normalizados()
        rutaGuardado = self.config['DEFAULT']['ruta_diccionario_idf_palabras']
        indice_pesos_offline = fich_pesosNorm_online.cargarEEDD_pesosNorm(rutaGuardado)
        indice_idf_offline = fich_pesosNorm_online.cargarEEDD_IDF(rutaGuardado)
        rutaGuardado = self.config['DEFAULT']['ruta_diccionario_palabras_invertidas']
        indice_dicc_palabras_invertidas = pares_palabra_frecuencia_online.cargarEEDD_diccPalabras_invertidas(rutaGuardado)
        indice_dicc_documentos_invertidas = pares_palabra_frecuencia_online.cargarEEDD_diccDocumentos_invertidas(rutaGuardado)
        #print(sorted(indice_pesos_offline.items()))
        vector_similitudes_consultas_doc = []
        similitud_docs_consulta = {}
        cont = 1
        for consulta in self.lista_consultas:
            #Calculo de los pesos normalizados por consulta
            pesos_palabras = fich_pesosNorm_online.pesos_palabras_consulta(indice_idf_offline, consulta, indice_dicc_palabras_invertidas)
            pesos_palabras_norm = fich_pesosNorm_online.normalizar_pesos_consulta(pesos_palabras)
            print("CONSULTA "+str(cont))
            cont += 1
            #Calculo de la similitud de la consulta con los documentos de la colección
            similitud_docs_consulta.clear()

            for id_doc in indice_dicc_documentos_invertidas: #Por cada documento
                sumatoria = 0.0
                for id_palabra in consulta: #Por cada palabra de la consulta
                    if indice_dicc_documentos_invertidas[id_doc] in indice_pesos_offline[indice_dicc_palabras_invertidas[id_palabra]]: #Si existe la palabra en el documento...
                        sumatoria = sumatoria + (pesos_palabras_norm[indice_dicc_palabras_invertidas[id_palabra]] * indice_pesos_offline[indice_dicc_palabras_invertidas[id_palabra]][indice_dicc_documentos_invertidas[id_doc]])
                        print("DOCUMENTO "+id_doc+" --> "+str(sumatoria))
        
        #print(vector_similitudes_consultas_doc)
            
        