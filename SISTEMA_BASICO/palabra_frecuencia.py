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
    
    def guardarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "wb") as tf:
            pickle.dump(self.dicc_palabrasFrec_archivos,tf)
        tf.close()
        sizefile = os.stat( join(rutaGuardado,"dicc_palabras_frecuencia.pkl")).st_size
        return sizefile
    
    def cargarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux