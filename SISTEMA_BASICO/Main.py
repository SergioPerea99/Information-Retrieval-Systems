from filtrado import Filtrado
import os
from os.path import isfile,join
import time

#VARIABLES NECESARIAS
rutaColeccion = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021"
contenido = os.listdir(rutaColeccion)
rutaLimpios = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Limpieza_SRI_2021"
archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
num_archivos = 0
sum_tokens = 0

#EJECUCION DE LA PRACTICA 1.1: Filtrado, Normalizacion y Tokenizacion.
start_time = time.time()
for archivo in archivos:
    filtro = Filtrado(join(rutaColeccion,archivo))
    sum_tokens += filtro.normalizacion_tokenizacion(rutaLimpios)
    num_archivos += 1
tiempo_ejecucion = time.time() - start_time

#DOCUMENTACION DEL PROGRAMA
documentacion_final = open("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\documentacion.txt",'w')
documentacion_final.write("El programa ha tardado "+str(tiempo_ejecucion)+" segundos en ejecutarse.\n")
documentacion_final.write("Total de archivos procesados -> "+str(num_archivos)+".\n")
documentacion_final.write("Total de tokens -> "+str(sum_tokens)+" :: Tokens/archivo -> "+str(sum_tokens/num_archivos)+".\n")
documentacion_final.close()