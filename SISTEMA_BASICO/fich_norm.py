# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:27:23 2021

@author: Sergio Perea
"""
import re, math
import pickle
import os
from os.path import join

class Ficheros_Pesos_Normalizados(object):
    
    def crear_IDF_palabras(self, dicc_palabras, total_lista_raices, num_documentos):
        idf_palabrasUnicas = {}
        for i in dicc_palabras: #Por cada palabra única
            cont = 0
            for j in total_lista_raices: #Por cada documento en formato de lista de palabras unicas en el documento
                if dicc_palabras[i] in j: #Comprobar si la palabra se encuentra en dicho documento
                    cont = cont + 1 
            idf_palabrasUnicas[i] = math.log(num_documentos/cont) #Añadir la palabra única y el número de documentos donde aparece
        return idf_palabrasUnicas
    
    
    def pesos_palabras_documento(self,ruta_archivos, idf_palabrasUnicas, dicc_archivos, dicc_palabras_invertido):
        dicc_palabrasDoc_pesos_sin_norm = {}
        for id_archivo in dicc_archivos:
            fichero = open(join(ruta_archivos,dicc_archivos[id_archivo]),"r")
            lista_palabras = []
            for linea in fichero:
                lista_palabras.append(re.sub('\n','',linea))
            fichero.close()
            
            #Se saca el numero de apariciones de la palabra en dicho archivo
            lista_palabra_frecuencia = []
            max_apariciones = -1
            for i in lista_palabras:
                if i not in lista_palabra_frecuencia:
                    apariciones = lista_palabras.count(i)
                    palabra_contador = [i, apariciones]
                    if max_apariciones < apariciones:
                        max_apariciones = apariciones
                    lista_palabra_frecuencia.append(palabra_contador)
            
            #print(dicc_palabras_invertido)
            for i in lista_palabra_frecuencia:
                i[1] = i[1]/max_apariciones #Esto es el tf(palabra,doc)
                #Se saca el peso de los terminos sin normalizar
                if i[0] in dicc_palabras_invertido:
                    w_palabra_doc = i[1] * idf_palabrasUnicas[dicc_palabras_invertido[i[0]]]
                    if not dicc_palabras_invertido[i[0]] in dicc_palabrasDoc_pesos_sin_norm:
                        dicc_palabrasDoc_pesos_sin_norm[dicc_palabras_invertido[i[0]]] = {id_archivo : w_palabra_doc}
                    else:
                        dicc_palabrasDoc_pesos_sin_norm[dicc_palabras_invertido[i[0]]][id_archivo] = w_palabra_doc 
        
        return dicc_palabrasDoc_pesos_sin_norm
    
    def pesos_palabras_consulta(self, idf_palabrasUnicas, consulta, dicc_palabras_invertido):
        
        #Se saca el numero de apariciones de la palabra en dicho archivo
        lista_palabra_frecuencia = []
        max_apariciones = -1
        for i in consulta:
            if i not in lista_palabra_frecuencia:
                apariciones = consulta.count(i)
                palabra_contador = [i, apariciones]
                if max_apariciones < apariciones:
                    max_apariciones = apariciones
                lista_palabra_frecuencia.append(palabra_contador)
        
        #Se saca el peso normalizado de la palabra en el archivo
        dicc_palabras_pesos_sin_norm = {}
        for i in lista_palabra_frecuencia:
            i[1] = i[1]/max_apariciones #Esto es el tf(palabra,doc)
            #Se saca el peso de los terminos sin normalizar
            if i[0] in dicc_palabras_invertido:
                w_palabra_consulta = i[1] * idf_palabrasUnicas[dicc_palabras_invertido[i[0]]]
                dicc_palabras_pesos_sin_norm[dicc_palabras_invertido[i[0]]] =  w_palabra_consulta
        return dicc_palabras_pesos_sin_norm
        
    
    def normalizar_pesos_documento(self,pesos_palabras_documento, dicc_archivos_invertido):
        dicc_pesos_palabrasDoc_norm = {}
        #Primero hago la sumatoria de pesos cuadráticos que hay en este documento
        for id_archivo in dicc_archivos_invertido: #Recorre los id de los archivos
            sumatoria = 0.0
            for i in pesos_palabras_documento: #Recorre los diccionarios de documentos por palabra
                if dicc_archivos_invertido[id_archivo] in pesos_palabras_documento[i]:
                    sumatoria = sumatoria + math.pow(pesos_palabras_documento[i][dicc_archivos_invertido[id_archivo]],2)
            denominador = math.sqrt(sumatoria)
            
            for i in pesos_palabras_documento:
                if dicc_archivos_invertido[id_archivo] in pesos_palabras_documento[i]:
                    if not i in dicc_pesos_palabrasDoc_norm:
                        dicc_pesos_palabrasDoc_norm[i] = {dicc_archivos_invertido[id_archivo] : pesos_palabras_documento[i][dicc_archivos_invertido[id_archivo]] / denominador }
                    else:
                        dicc_pesos_palabrasDoc_norm[i][dicc_archivos_invertido[id_archivo]] = pesos_palabras_documento[i][dicc_archivos_invertido[id_archivo]] / denominador 
                        
        return dicc_pesos_palabrasDoc_norm
    
    def normalizar_pesos_consulta(self,pesos_palabras):
        #Primero hago la sumatoria de pesos cuadráticos que hay en este documento
        sumatoria = 0.0
        for i in pesos_palabras: #Recorre los diccionarios de documentos por palabra
            sumatoria = sumatoria + math.pow(pesos_palabras[i],2)
        denominador = math.sqrt(sumatoria)
        
        dicc_pesos_palabras_norm = {}
        for i in pesos_palabras:
            dicc_pesos_palabras_norm[i] = pesos_palabras[i] / denominador 
        return dicc_pesos_palabras_norm
    
    def guardarEEDD_pesosNorm(self,rutaGuardado, pesos_palabrasDoc_norm):
        with open(join(rutaGuardado,"dicc_pesosNormalizados.pkl"), "wb") as tf:
            pickle.dump(pesos_palabrasDoc_norm,tf)
        tf.close()
        sizefile = os.stat( join(rutaGuardado,"dicc_pesosNormalizados.pkl")).st_size
        return sizefile
        
    def guardarEEDD_IDF(self,rutaGuardado, idf_palabrasUnicas):
        with open(join(rutaGuardado,"dicc_IDF.pkl"), "wb") as tf:
            pickle.dump(idf_palabrasUnicas,tf)
        tf.close()
        sizefile = os.stat( join(rutaGuardado,"dicc_IDF.pkl")).st_size
        return sizefile
    
        
    def cargarEEDD_pesosNorm(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_pesosNormalizados.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux

    def cargarEEDD_IDF(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_IDF.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux