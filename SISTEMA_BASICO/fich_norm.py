# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:27:23 2021

@author: Sergio Perea
"""
import re

class Ficheros_Pesos_Normalizados(object):
    
    def normalizar_pesos_archivo(self,ruta_archivo):
        fichero = open(ruta_archivo,"r")
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
        
        #Se saca el peso normalizado de la palabra en el archivo
        for i in lista_palabra_frecuencia:
            i[1] = i[1]/max_apariciones
            print(i)
        return lista_palabra_frecuencia