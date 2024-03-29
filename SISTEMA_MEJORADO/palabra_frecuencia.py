# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:25:22 2021

@author: Sergio Perea
"""
import os
import pickle
from os.path import isfile,join

class Pares_Palabra_Frecuencia:
    
    #Constructor por defecto
    def __init__(self):
        self.identificador = 1
        self.dicc_archivos = {}
        self.dicc_palabras = {}
        self.dicc_palabrasFrec_archivos = {}
        self.dicc_palabras_invertida = {}
        self.dicc_archivos_invertida = {}
        self.dicc_archivosFrec_palabras = {}
        
    #Creación de diccionario de palabras únicas
    def dicc_terminos(self, lista_palabras_unicas):
        for i in lista_palabras_unicas:
            self.dicc_palabras[self.identificador] = i
            self.dicc_palabras_invertida[i] = self.identificador
            self.identificador = self.identificador + 1
        return self.dicc_palabras
    
    def get_dicc_invert_terminos(self):
        return self.dicc_palabras_invertida
    
    #Creación de diccionario de los nombres de los ficheros
    def dicc_ficheros(self, ruta_coleccion):
        contenido = os.listdir(ruta_coleccion)
        archivos = [nombre for nombre in contenido if isfile(join(ruta_coleccion,nombre))] #Obtener los archivos de la carpeta
        for archivo in archivos:
            self.dicc_archivos[self.identificador] = archivo
            self.dicc_archivos_invertida[archivo] = self.identificador
            self.identificador = self.identificador + 1
        return self.dicc_archivos
    
    def get_dicc_invert_archivos(self):
        return self.dicc_archivos_invertida
    
    #Creación de diccionario de los nombres de los ficheros
    def crearEEDD_palabrasFrecuencia(self, ruta_coleccion): 
        for key_fichero in self.dicc_archivos:
            archivo = open(join(ruta_coleccion,self.dicc_archivos[key_fichero]),"r") 
            for linea in archivo:
                clavePalabra = self.dicc_palabras_invertida[linea.strip()]
                if clavePalabra in self.dicc_palabrasFrec_archivos: #Comprobar si existe la palabra en el dicc
                    if key_fichero in self.dicc_palabrasFrec_archivos[clavePalabra]: #Comprobar si existe ya una aparicion de la palabra en dicho fichero
                        self.dicc_palabrasFrec_archivos[clavePalabra][key_fichero] = self.dicc_palabrasFrec_archivos[clavePalabra][key_fichero] + 1 #Incrementar en 1 su aparicion en cierto caso
                    else:
                        self.dicc_palabrasFrec_archivos[clavePalabra][key_fichero] = 1
                else:
                    self.dicc_palabrasFrec_archivos[clavePalabra] = {key_fichero: 1}
            archivo.close()
        return self.dicc_palabrasFrec_archivos
    
    #Pr2: Creación de por cada documento, las palabras y su frecuencia de aparición
    def crearEEDD_documentosFrecuenciaPalabras(self, ruta_coleccion):
        for key_fichero in self.dicc_archivos:
            archivo = open(join(ruta_coleccion,self.dicc_archivos[key_fichero]),"r")
            for linea in archivo:
                clavePalabra = self.dicc_palabras_invertida[linea.strip()]
                if key_fichero in self.dicc_archivosFrec_palabras: #Comprobar si existe el fichero en el dicc  
                    if clavePalabra in self.dicc_archivosFrec_palabras[key_fichero]: #Comprobar si existe ya una aparicion de la palabra en dicho fichero
                        self.dicc_archivosFrec_palabras[key_fichero][clavePalabra] = self.dicc_archivosFrec_palabras[key_fichero][clavePalabra] + 1 #Incrementar en 1 su aparicion en cierto caso
                    else:
                        self.dicc_archivosFrec_palabras[key_fichero][clavePalabra] = 1
                else:
                    self.dicc_archivosFrec_palabras[key_fichero] = {clavePalabra: 1}
            archivo.close()
        return self.dicc_archivosFrec_palabras
                
    def guardarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "wb") as tf:
            pickle.dump(self.dicc_palabrasFrec_archivos,tf)
        tf.close()
        sizefile = os.stat( join(rutaGuardado,"dicc_palabras_frecuencia.pkl")).st_size
        return sizefile
    
    def guardarEEDD_documentosFrecuenciaPalabras(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_documentos_frecuencia.pkl"), "wb") as tf:
            pickle.dump(self.dicc_archivosFrec_palabras,tf)
        tf.close()
        
    
    def guardarEEDD_diccPalabras(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras.pkl"), "wb") as tf:
            pickle.dump(self.dicc_palabras,tf)
        tf.close()
    
    def guardarEEDD_diccArchivos(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_archivos.pkl"), "wb") as tf:
            pickle.dump(self.dicc_archivos,tf)
        tf.close()
    
    def guardarEEDD_diccPalabras_invertidas(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_invertidas.pkl"), "wb") as tf:
            pickle.dump(self.dicc_palabras_invertida,tf)
        tf.close()
    
    def guardarEEDD_diccDocumentos_invertidas(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_documentos_invertidas.pkl"), "wb") as tf:
            pickle.dump(self.dicc_archivos_invertida,tf)
        tf.close()
    
    
    def cargarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux
    
    def cargarEEDD_documentosFrecuenciaPalabras(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_documentos_frecuencia.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux
    
    
    def cargarEEDD_diccPalabras(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux
    
    def cargarEEDD_diccArchivos(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_archivos.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux
    
    def cargarEEDD_diccPalabras_invertidas(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_invertidas.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux
    
    def cargarEEDD_diccDocumentos_invertidas(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_documentos_invertidas.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux