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
from xml.dom import minidom


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
        
        #De lista de listas a lista
        aux = []
        for i in self.lista_consultas:
            if type(i) is list:
                for palabra in i:
                    aux.append(palabra)
            else:
                 aux.append(i)
        self.lista_consultas = aux.copy()
        
        
    
    def procesar_pesos(self):
        self.pares_palabra_frecuencia_online = Pares_Palabra_Frecuencia()
        self.fich_pesosNorm_online = Ficheros_Pesos_Normalizados()
        rutaGuardado = self.config['OFFLINE']['ruta_coleccion_ficherosNormalizados']
        self.indice_pesos_offline = self.fich_pesosNorm_online.cargarEEDD_pesosNorm(rutaGuardado)
        self.indice_idf_offline = self.fich_pesosNorm_online.cargarEEDD_IDF(rutaGuardado)
        rutaGuardado = self.config['OFFLINE']['ruta_diccionarios_invertidos']
        self.indice_dicc_palabras_invertidas = self.pares_palabra_frecuencia_online.cargarEEDD_diccPalabras_invertidas(rutaGuardado)
        self.indice_dicc_documentos_invertidas = self.pares_palabra_frecuencia_online.cargarEEDD_diccDocumentos_invertidas(rutaGuardado)
        rutaGuardado = self.config['OFFLINE']['ruta_diccionario_archivos']
        self.indice_dicc_documentos = self.pares_palabra_frecuencia_online.cargarEEDD_diccArchivos(rutaGuardado)
        rutaGuardado = self.config['OFFLINE']['ruta_diccionario_palabras']
        self.dicc_palabras = self.pares_palabra_frecuencia_online.cargarEEDD_diccPalabras(rutaGuardado)
        
        
        cont = 1
        ruta_fichero_resultados = self.config['ONLINE']['ruta_ficheros_consultas_resultados']
        ruta_fichero_resultados_ordenados = self.config['ONLINE']['ruta_ficheros_consultas_resultados_ordenados']
        #Calculo de los pesos normalizados por consulta
        pesos_palabras = self.fich_pesosNorm_online.pesos_palabras_consulta(self.indice_idf_offline, self.lista_consultas, self.indice_dicc_palabras_invertidas)
        self.pesos_palabras_norm = self.fich_pesosNorm_online.normalizar_pesos_consulta(pesos_palabras)
        
        archivo = open(join(ruta_fichero_resultados,"consulta"+str(cont)+".txt"),"w")
        archivo2 = open(join(ruta_fichero_resultados_ordenados,"consulta"+str(cont)+".txt"),"w")
        
        #Calculo de la similitud de la consulta con los documentos de la colección
        self.similitud_docs_consulta = {}


        start_time = time.time()
        for id_doc in self.indice_dicc_documentos_invertidas: #Por cada documento
            sumatoria = 0.0
            for id_palabra in self.lista_consultas: #Por cada palabra de la consulta
                if id_palabra in self.indice_dicc_palabras_invertidas:
                    if self.indice_dicc_documentos_invertidas[id_doc] in self.indice_pesos_offline[self.indice_dicc_palabras_invertidas[id_palabra]]: #Si existe la palabra en el documento...
                        sumatoria = sumatoria + (self.pesos_palabras_norm[self.indice_dicc_palabras_invertidas[id_palabra]] * self.indice_pesos_offline[self.indice_dicc_palabras_invertidas[id_palabra]][self.indice_dicc_documentos_invertidas[id_doc]])
                else:
                    self.lista_consultas.remove(id_palabra) #ELIMINAR LA PALABRA QUE NO EXISTE EN EL VOCABULARIO DE TÉRMINOS CREADO DE FORMA OFFLINE 
                    
            if sumatoria > 0:
                self.similitud_docs_consulta[self.indice_dicc_documentos_invertidas[id_doc]] = sumatoria
                archivo.write(str(id_doc)+" --> similitud = "+str(sumatoria)+"\n")
        tiempo_ejecucion = time.time() - start_time
        archivo.write("------ TIEMPO EN SEGUNDOS EN CALCULAR LA SIMILITUD PARA LOS DOCUMENTOS = "+str(tiempo_ejecucion)+" ------\n")
        
        self.similitud_docs_consulta = sorted(self.similitud_docs_consulta.items(),reverse = True, key=operator.itemgetter(1))
        
        #print(self.similitud_docs_consulta)
        archivo.close()
        
        archivo2.write("Consulta: "+self.dicc_consultas[cont])
        
        
        i = 0
        for id_doc in self.similitud_docs_consulta:
            if i < self.doc_max:
                contenido_archivo = self.mostrarContenidoArchivo(self.indice_dicc_documentos[id_doc[0]])
                archivo2.write(str(contenido_archivo[0])+"\n"+str(contenido_archivo[1])+"\n"+str(contenido_archivo[2])+"\n")
            else:
                break
            i += 1
        cont += 1
    
        archivo2.close()
        
       
    
    def pseudorealimentacion_prf(self,num_docs_relevantes, num_palabras_frecuentes):
        #Tengo el diccionario de por cada palabra de la colección, aparece la frecuencia que tiene ésta sobre cada uno de los documentos donde aparece...
        rutaDiccionario = self.config['OFFLINE']['ruta_almacen_documentos_frecuencia_palabras']
        dicc_documentos_frec_palabras = self.pares_palabra_frecuencia_online.cargarEEDD_documentosFrecuenciaPalabras(rutaDiccionario)
        
        i = 0
        for doc_peso in self.similitud_docs_consulta:
            if i < num_docs_relevantes:
                dicc_orden_palabras_doc = dicc_documentos_frec_palabras[doc_peso[0]].copy()
                dicc_orden_palabras_doc = sorted(dicc_orden_palabras_doc.items(),reverse = True, key=operator.itemgetter(1))
                j = 0
                for palabra in dicc_orden_palabras_doc:
                    if j < num_palabras_frecuentes:
                        self.lista_consultas.append(self.dicc_palabras[palabra[0]])
                    else:
                        break
                    j += 1
            else:
                break
            i += 1
        
        
        #Ahora se vuelve a hacer el cálculo de los pesos
        self.procesar_pesos()
        
    
    
    def mostrarContenidoArchivo(self,nombre_archivo):
        rutaColeccion = self.config['OFFLINE']['ruta_coleccion_inicio']
        nombre_archivo = nombre_archivo.split(".")
        nombre_archivo = nombre_archivo[0] + ".xml"
        doc = minidom.parse(join(rutaColeccion,nombre_archivo))
        titulo = doc.getElementsByTagName("dc:title")[0]
        introduccion = doc.getElementsByTagName("dc:description")[0]
        url = doc.getElementsByTagName("dc:identifier")[0]
        titulo = titulo.firstChild.data
        introduccion = introduccion.firstChild.data
        url = url.firstChild.data
        return [str(url), str(titulo),str(introduccion)]
    
    def getListaConsulta(self):
        return self.lista_consultas
    
    def getPesosPalabrasConsulta(self):
        lista = []
        for i in self.pesos_palabras_norm:
            lista.append([self.dicc_palabras[i],self.pesos_palabras_norm[i]])
        return lista