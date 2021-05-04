# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:09:30 2021

@author: Sergio Perea
"""
from filtrado import Filtrado
from stopper import Stopper
from stemmer import Stemmer
from palabra_frecuencia import Pares_Palabra_Frecuencia
from fich_norm import Ficheros_Pesos_Normalizados
from os.path import join
import time
import operator

class Buscador(object):
    
    #Constructor por defecto
    def __init__(self, config, fich_consultas, doc_max):
        self.config = config
        self.fich_consultas = fich_consultas
        self.doc_max = doc_max
        filtro = Filtrado(self.fich_consultas)
        ruta_destino = config['ONLINE']['ruta_fich_consultas_modificadas']
        
        #Diccionario con la frase y la consulta
        self.dicc_consultas = {}
        cont = 1
        for i in filtro.informacion:
            self.dicc_consultas[cont] = i
            cont += 1
        
        #Hace la parte de normalización
        filtro.normalizacion_tokenizacion(ruta_destino)
        
        #Hace la parte de stopper
        lista_stopword = config['OFFLINE']['ruta_lista_stopword']
        vacias = Stopper(lista_stopword) #Crear el stopper
        vacias.eliminacion_vacias(ruta_destino,ruta_destino) #Eliminar palabra vacía
        
        #Hace la parte de stemmer
        raices = Stemmer()
        lista_palabras_consulta = raices.extraccion_raices(ruta_destino, ruta_destino)
        lista_aux = []
        self.lista_consultas = []
        i = 0
        while i < len(lista_palabras_consulta[1]):
            if not lista_palabras_consulta[1][i]  == '':
                lista_aux.append(lista_palabras_consulta[1][i])
                if i == len(lista_palabras_consulta[1])-1:
                    self.lista_consultas.append(lista_aux.copy())
                    lista_aux.clear()
            else:
                self.lista_consultas.append(lista_aux.copy())
                lista_aux.clear()
            i += 1
    
    def procesar_pesos(self):
        pares_palabra_frecuencia_online = Pares_Palabra_Frecuencia()
        fich_pesosNorm_online = Ficheros_Pesos_Normalizados()
        rutaGuardado = self.config['OFFLINE']['ruta_coleccion_ficherosNormalizados']
        indice_pesos_offline = fich_pesosNorm_online.cargarEEDD_pesosNorm(rutaGuardado)
        indice_idf_offline = fich_pesosNorm_online.cargarEEDD_IDF(rutaGuardado)
        rutaGuardado = self.config['OFFLINE']['ruta_diccionarios_invertidos']
        indice_dicc_palabras_invertidas = pares_palabra_frecuencia_online.cargarEEDD_diccPalabras_invertidas(rutaGuardado)
        indice_dicc_documentos_invertidas = pares_palabra_frecuencia_online.cargarEEDD_diccDocumentos_invertidas(rutaGuardado)
        rutaGuardado = self.config['OFFLINE']['ruta_diccionario_archivos']
        indice_dicc_documentos = pares_palabra_frecuencia_online.cargarEEDD_diccArchivos(rutaGuardado)
        
        
        cont = 1
        ruta_fichero_resultados = self.config['ONLINE']['ruta_ficheros_consultas_resultados']
        for consulta in self.lista_consultas:
            #Calculo de los pesos normalizados por consulta
            pesos_palabras = fich_pesosNorm_online.pesos_palabras_consulta(indice_idf_offline, consulta, indice_dicc_palabras_invertidas)
            pesos_palabras_norm = fich_pesosNorm_online.normalizar_pesos_consulta(pesos_palabras)
            
            archivo = open(join(ruta_fichero_resultados,"consulta"+str(cont)+".txt"),"w")
            
            #Calculo de la similitud de la consulta con los documentos de la colección
            similitud_docs_consulta = {}


            start_time = time.time()
            for id_doc in indice_dicc_documentos_invertidas: #Por cada documento
                sumatoria = 0.0
                for id_palabra in consulta: #Por cada palabra de la consulta
                    if indice_dicc_documentos_invertidas[id_doc] in indice_pesos_offline[indice_dicc_palabras_invertidas[id_palabra]]: #Si existe la palabra en el documento...
                        sumatoria = sumatoria + (pesos_palabras_norm[indice_dicc_palabras_invertidas[id_palabra]] * indice_pesos_offline[indice_dicc_palabras_invertidas[id_palabra]][indice_dicc_documentos_invertidas[id_doc]])
                
                if sumatoria > 0:
                    similitud_docs_consulta[indice_dicc_documentos_invertidas[id_doc]] = sumatoria
                    archivo.write(str(id_doc)+" --> similitud = "+str(sumatoria)+"\n")
            tiempo_ejecucion = time.time() - start_time
            archivo.write("------ TIEMPO EN SEGUNDOS EN CALCULAR LA SIMILITUD PARA LOS DOCUMENTOS = "+str(tiempo_ejecucion)+" ------\n")
            archivo.close()
            
            similitud_docs_consulta = sorted(similitud_docs_consulta.items(),reverse = True, key=operator.itemgetter(1))
            #SALIDA POR PANTALLA DE LOS N DOCUMENTOS CON MAYOR SIMILITUD 
            print("\nConsulta "+str(cont)+": "+self.dicc_consultas[cont])
            
            i = 0
            for id_doc in similitud_docs_consulta:
                if i < self.doc_max:
                    print(str(id_doc[1])+" "+str(indice_dicc_documentos[id_doc[0]]))
                else:
                    break
                i += 1
            cont += 1
        
            
        