from stopper import Stopper
from filtrado import Filtrado
import os
from os.path import isfile,join
import time


#EJECUCION DE LA PRACTICA 1.1: Filtrado, Normalizacion y Tokenizacion.
#---VARIABLES NECESARIAS
rutaColeccion = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021"
contenido = os.listdir(rutaColeccion)
ruta_destino = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Limpieza_SRI_2021"
archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
num_archivos = len(archivos)
sum_tokens = 0
minimo_palabras = 9999999
maximo_palabras = -1

#---EJECUCION DE LOS MÉTODOS
start_time = time.time()
for archivo in archivos:
    filtro = Filtrado(join(rutaColeccion,archivo))
    num_tokens = filtro.normalizacion_tokenizacion(ruta_destino)
    if minimo_palabras > num_tokens: minimo_palabras = num_tokens
    if maximo_palabras < num_tokens: maximo_palabras = num_tokens
    sum_tokens += num_tokens
tiempo_ejecucion = time.time() - start_time

#ABRIR EL DOCUMENTO DE LAS MEMORIAS
documentacion_final = open("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\documentacion.txt",'w')
documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.1 --------------"+"\n")
documentacion_final.write("El programa ha tardado "+str(tiempo_ejecucion)+" segundos en ejecutarse.\n")
documentacion_final.write("Total de archivos procesados -> "+str(num_archivos)+".\n")
documentacion_final.write("Total de tokens -> "+str(sum_tokens)+" :: Tokens/archivo -> "+str(sum_tokens/num_archivos)+".\n")
documentacion_final.write("Número MÍNIMO de palabras una vez normalizado y tokenizado -> "+str(minimo_palabras)+"\n")
documentacion_final.write("Número MÁXIMO de palabras una vez normalizado y tokenizado -> "+str(maximo_palabras)+"\n")


#EJECUCION DE LA PRACTICA 1.2: Eliminación de palabras vacías.
rutaColeccion = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Limpieza_SRI_2021"
lista_stopword = "spanishSmart.txt"
contenido = os.listdir(rutaColeccion)
ruta_destino = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\stopper"
archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
vacias = Stopper(join("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO",lista_stopword)) #Crear el stopper
total_palabras_no_vacias = 0
minimo_palabras = 9999999
maximo_palabras = -1

for archivo in archivos:
    palabrasDoc_no_vacias = vacias.eliminacion_vacias(join(rutaColeccion,archivo),join(ruta_destino,archivo)) #Eliminar palabra vacía
    if minimo_palabras > palabrasDoc_no_vacias: minimo_palabras = palabrasDoc_no_vacias
    if maximo_palabras < palabrasDoc_no_vacias: maximo_palabras = palabrasDoc_no_vacias
    total_palabras_no_vacias += palabrasDoc_no_vacias

documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.2 --------------"+"\n")
documentacion_final.write("Listado de Stopword seleccionado -> "+lista_stopword+"\n")
documentacion_final.write("Número TOTAL de palabras una vez limpiada de palabras vacias -> "+str(total_palabras_no_vacias)+"\n")
documentacion_final.write("Número MÍNIMO de palabras una vez limpiada de palabras vacias -> "+str(minimo_palabras)+"\n")
documentacion_final.write("Número MÁXIMO de palabras una vez limpiada de palabras vacias -> "+str(maximo_palabras)+"\n")
documentacion_final.write("Número MEDIO de palabras por documento -> "+str(total_palabras_no_vacias/num_archivos)+"\n")


#CERRAR EL DOCUMENTO DE LAS MEMORIAS
documentacion_final.close()