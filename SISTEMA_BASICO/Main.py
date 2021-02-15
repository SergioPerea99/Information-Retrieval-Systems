
from filtrado import Filtrado
import os
from os.path import isfile,join
import time

rutaColeccion = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021"
contenido = os.listdir(rutaColeccion)
rutaLimpios = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Limpieza_SRI_2021"

#Obtener los archivos de la carpeta
archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))]

start_time = time.time()
for archivo in archivos:
    filtro = Filtrado(join(rutaColeccion,archivo))
    filtro.normalizacion_tokenizacion(rutaLimpios)
print("El programa ha tardado ",(time.time() - start_time), " segundos en ejecutarse")