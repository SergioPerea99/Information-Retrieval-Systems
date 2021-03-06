from stopper import Stopper
from filtrado import Filtrado
import os
from os.path import isfile,join
import time
from nltk.stem import PorterStemmer
from operator import itemgetter, attrgetter
#---------------------------------------------------------------------
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
coleccion_palabras_normalizadas = []
#---EJECUCION DE LOS MÉTODOS
#Tiempo de cargar las palabras normalizadas en nuevos ficheros
start_time = time.time()
for archivo in archivos:
    filtro = Filtrado(join(rutaColeccion,archivo))
    palabras_normalizadas = filtro.normalizacion_tokenizacion(ruta_destino)
    if minimo_palabras > palabras_normalizadas[0]: minimo_palabras = palabras_normalizadas[0]
    if maximo_palabras < palabras_normalizadas[0]: maximo_palabras = palabras_normalizadas[0]
    sum_tokens += palabras_normalizadas[0]
    coleccion_palabras_normalizadas.append(palabras_normalizadas[1])
tiempo_ejecucion = time.time() - start_time


#Generar las 5 palabras de mayor frecuencia
listaPalabras_normalizadas = []
for lista_palabras in coleccion_palabras_normalizadas: #AGRUPAR TODAS LAS PALABRAS EN UNA MISMA LISTA
    listaPalabras_normalizadas = listaPalabras_normalizadas + lista_palabras

palabrasUnicas = []
for w in listaPalabras_normalizadas: #ELIMINAR LAS PALABRAS REPETIDAS EN OTRA LISTA
    if not w in palabrasUnicas:
        palabrasUnicas.append(w)
        
frecuenciaPalab = []    
for w in palabrasUnicas: #CONTADOR DE CADA PALABRA (UNICA) DESDE LA LISTA QUE CONTIENE TODAS LAS PALABRAS (REPETIDAS)
    frecuenciaPalab.append(listaPalabras_normalizadas.count(w))
    
pair_palabras_frecuencia = list(zip(palabrasUnicas,frecuenciaPalab))
pair_palabras_frecuencia = sorted(pair_palabras_frecuencia, key=itemgetter(1), reverse=True)

palabras_mayorFrecuencia = []
palabras_frecuenciaColeccion = []
for i in range(5):
    palabras_frecuenciaColeccion.append(pair_palabras_frecuencia[i][1]/len(palabrasUnicas))
    palabras_mayorFrecuencia.append(pair_palabras_frecuencia[i])

palabras5_mayorFrec = list(zip(palabras_mayorFrecuencia,palabras_frecuenciaColeccion))
#print(str(palabras5_mayorFrec))


#---ABRIR EL DOCUMENTO DE LAS MEMORIAS
documentacion_final = open("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\documentacion.txt",'w')
documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.1 --------------"+"\n")
documentacion_final.write("El programa ha tardado "+str(tiempo_ejecucion)+" segundos en ejecutarse.\n")
documentacion_final.write("Total de archivos procesados -> "+str(num_archivos)+".\n")
documentacion_final.write("Total de tokens -> "+str(sum_tokens)+" :: Tokens/archivo -> "+str(sum_tokens/num_archivos)+".\n")
documentacion_final.write("Número MÍNIMO de palabras una vez normalizado y tokenizado -> "+str(minimo_palabras)+"\n")
documentacion_final.write("Número MÁXIMO de palabras una vez normalizado y tokenizado -> "+str(maximo_palabras)+"\n")
documentacion_final.write("Número MEDIO de palabras por documento -> "+str(sum_tokens/num_archivos)+"\n")
documentacion_final.write("Las 5 palabras más frecuentes -> "+str(palabras5_mayorFrec)+"\n")



#---------------------------------------------------------------------
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
    if minimo_palabras > len(palabrasDoc_no_vacias): minimo_palabras = len(palabrasDoc_no_vacias)
    if maximo_palabras < len(palabrasDoc_no_vacias): maximo_palabras = len(palabrasDoc_no_vacias)
    total_palabras_no_vacias += len(palabrasDoc_no_vacias)


#Generar las 5 palabras de mayor frecuencia
palabrasUnicas.clear()
for w in palabrasDoc_no_vacias: #ELIMINAR LAS PALABRAS REPETIDAS EN OTRA LISTA
    if not w in palabrasUnicas:
        palabrasUnicas.append(w)
        
frecuenciaPalab.clear()   
for w in palabrasUnicas: #CONTADOR DE CADA PALABRA (UNICA) DESDE LA LISTA QUE CONTIENE TODAS LAS PALABRAS (REPETIDAS)
    frecuenciaPalab.append(palabrasDoc_no_vacias.count(w))

pair_palabras_frecuencia = list(zip(palabrasUnicas,frecuenciaPalab))
pair_palabras_frecuencia = sorted(pair_palabras_frecuencia, key=itemgetter(1), reverse=True)

palabras_mayorFrecuencia = []
palabras_frecuenciaColeccion = []
for i in range(5):
    palabras_frecuenciaColeccion.append(pair_palabras_frecuencia[i][1]/len(palabrasUnicas))
    palabras_mayorFrecuencia.append(pair_palabras_frecuencia[i])

palabras5_mayorFrec = list(zip(palabras_mayorFrecuencia,palabras_frecuenciaColeccion))


documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.2 --------------"+"\n")
documentacion_final.write("Listado de Stopword seleccionado -> "+lista_stopword+"\n")
documentacion_final.write("Número TOTAL de palabras una vez limpiada de palabras vacias -> "+str(total_palabras_no_vacias)+"\n")
documentacion_final.write("Número MÍNIMO de palabras una vez limpiada de palabras vacias -> "+str(minimo_palabras)+"\n")
documentacion_final.write("Número MÁXIMO de palabras una vez limpiada de palabras vacias -> "+str(maximo_palabras)+"\n")
documentacion_final.write("Número MEDIO de palabras por documento -> "+str(total_palabras_no_vacias/num_archivos)+"\n")
documentacion_final.write("Las 5 palabras más frecuentes -> "+str(palabras5_mayorFrec)+"\n")


#---------------------------------------------------------------------
#EJECUCIÓN DE LA PRÁCTICA 1.3: STEMMER CON PORTER.
#TODO: - Antes de usar el stemmer es necesario quitar los "\n" de las palabras de los ficheros para que lo pueda reconocer.


#CERRAR EL DOCUMENTO DE LAS MEMORIAS
documentacion_final.close()