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
        
    #Creación de diccionario de palabras únicas
    def dicc_terminos(self, lista_palabras_unicas):
        for i in lista_palabras_unicas:
            self.dicc_palabras[self.identificador] = i
            self.identificador = self.identificador + 1
        return self.dicc_palabras
    
    #Creación de diccionario de los nombres de los ficheros
    def dicc_ficheros(self, ruta_coleccion):
        contenido = os.listdir(ruta_coleccion)
        archivos = [nombre for nombre in contenido if isfile(join(ruta_coleccion,nombre))] #Obtener los archivos de la carpeta
        for archivo in archivos:
            self.dicc_archivos[self.identificador] = archivo
            self.identificador = self.identificador + 1
        return self.dicc_archivos
    
    #Creación de diccionario de los nombres de los ficheros
    def crearEEDD_palabrasFrecuencia(self, ruta_coleccion): 
        for key_palabra in self.dicc_palabras:
            for key_fichero in self.dicc_archivos:
                archivo = open(join(ruta_coleccion,self.dicc_archivos[key_fichero]),"r") 
                lineas = [linea.strip() for linea in archivo]
                archivo.close()
                apariciones = lineas.count(self.dicc_palabras[key_palabra])
                if apariciones > 0:
                    self.dicc_palabrasFrec_archivos[key_palabra] = {key_fichero: apariciones}
        return self.dicc_palabrasFrec_archivos
    
    def guardarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "wb") as tf:
            pickle.dump(self.dicc_palabrasFrec_archivos,tf)
        tf.close()
    def cargarEEDD_palabrasFrecuencia(self,rutaGuardado):
        with open(join(rutaGuardado,"dicc_palabras_frecuencia.pkl"), "rb") as tf:
            aux = pickle.load(tf)
        tf.close()
        return aux