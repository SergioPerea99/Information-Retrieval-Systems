
from filtrado import Filtrado
import os
from os.path import isfile,join

ruta = "C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021"
contenido = os.listdir(ruta)

#Obtener los archivos de la carpeta
archivos = [nombre for nombre in contenido if isfile(join(ruta,nombre))]
#print(archivos)

for archivo in archivos:
    filtro = Filtrado(join(ruta,archivo))
    filtro.normalizacion_tokenizacion()
