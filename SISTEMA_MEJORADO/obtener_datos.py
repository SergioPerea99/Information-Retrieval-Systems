# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:19:18 2021

@author: Sergio Perea
"""



import os
import cgi
import configparser
from buscador import Buscador
from os.path import join




# Headers
print("Content-Type: text/html")
print()
print("<html>")
buscador_input = cgi.FieldStorage()

if "name" not in buscador_input:
    print("<h1>NO HA ESCRITO NADA PARA BUSCAR.</h1>")
    print("<h2>POR FAVOR, ESCRIBA ALGO ANTES DE DAR AL BOTÓN DE BUSCAR.</h2>")
else:
    #TENEMOS LA FRASE, HAY QUE ESCRIBIR EN EL TEXTO DE LA CONSULTA.TXT Y LUEGO EJECUTAR LA PARTE ONLINE DEL SRI.
    
    config = configparser.ConfigParser()
    config.read('conf.ini')
    
    ruta_fichero_consultas = config['ONLINE']['ruta_fich_consultas']
    archivo = open(ruta_fichero_consultas,"w")
    archivo.write(str(buscador_input["name"].value)+"\n")
    archivo.close()
    
    buscador = Buscador(config,ruta_fichero_consultas,5)
    buscador.procesar_pesos()
    
    rutaColeccion = config['ONLINE']['ruta_ficheros_consultas_resultados_ordenados']
    contenido = os.listdir(rutaColeccion)
    
    archivos = [join(rutaColeccion,nombre) for nombre in contenido]
    
    for consulta in archivos:
        fichero = open(consulta,"r")
        for linea in fichero:
            print("<p>%s</p>" % (linea))
        fichero.close()
   
print("</html>")