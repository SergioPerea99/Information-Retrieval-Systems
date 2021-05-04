from stopper import Stopper
from filtrado import Filtrado
from stemmer import Stemmer
from palabra_frecuencia import Pares_Palabra_Frecuencia
from fich_norm import Ficheros_Pesos_Normalizados
from buscador import Buscador
from os.path import isfile,join
from operator import itemgetter
import os
import time
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')

ejecucion_offline = False


if ejecucion_offline:
    #---------------------------------------------------------------------
    #EJECUCION DE LA PRACTICA 1.1: Filtrado, Normalizacion y Tokenizacion.
    #---VARIABLES NECESARIAS
    rutaColeccion = config['OFFLINE']['ruta_coleccion_inicio']
    contenido = os.listdir(rutaColeccion)
    ruta_destino = config['OFFLINE']['ruta_coleccion_normalizada']
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
    
    
    #---ABRIR EL DOCUMENTO DE LAS MEMORIAS
    ruta_archivo_historial = config['OFFLINE']['ruta_archivo_historial']
    documentacion_final = open(ruta_archivo_historial,'w')
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
    rutaColeccion = ruta_destino
    lista_stopword = config['OFFLINE']['ruta_lista_stopword']
    contenido = os.listdir(rutaColeccion)
    ruta_destino = config['OFFLINE']['ruta_coleccion_stopper']
    archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
    vacias = Stopper(lista_stopword) #Crear el stopper
    minimo_palabras = 9999999
    maximo_palabras = -1
    
    palabrasDoc_no_vacias = []
    for archivo in archivos:
        palabrasDoc = vacias.eliminacion_vacias(join(rutaColeccion,archivo),join(ruta_destino,archivo)) #Eliminar palabra vacía
        if minimo_palabras > len(palabrasDoc): minimo_palabras = len(palabrasDoc)
        if maximo_palabras < len(palabrasDoc): maximo_palabras = len(palabrasDoc)
        palabrasDoc_no_vacias = palabrasDoc_no_vacias + palabrasDoc
    
    
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
    documentacion_final.write("Número TOTAL de palabras una vez limpiada de palabras vacias -> "+str(len(palabrasDoc_no_vacias))+"\n")
    documentacion_final.write("Número MÍNIMO de palabras una vez limpiada de palabras vacias -> "+str(minimo_palabras)+"\n")
    documentacion_final.write("Número MÁXIMO de palabras una vez limpiada de palabras vacias -> "+str(maximo_palabras)+"\n")
    documentacion_final.write("Número MEDIO de palabras por documento -> "+str(len(palabrasDoc_no_vacias)/num_archivos)+"\n")
    documentacion_final.write("Las 5 palabras más frecuentes -> "+str(palabras5_mayorFrec)+"\n")
    
    
    #---------------------------------------------------------------------
    #EJECUCIÓN DE LA PRÁCTICA 1.3: STEMMER CON PORTER.
    rutaColeccion = config['OFFLINE']['ruta_coleccion_stopper']
    contenido = os.listdir(rutaColeccion)
    ruta_destino = config['OFFLINE']['ruta_coleccion_stemmer']
    raices = Stemmer()
    archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
    minimo_palabras = 9999999
    maximo_palabras = -1
    
    total_lista_raices_sinRepeticiones = []
    total_lista_raices_conRepeticiones = []
    total_lista_raices = []
    for archivo in archivos:
        lista_raices = raices.extraccion_raices(join(rutaColeccion,archivo),join(ruta_destino,archivo))
        if minimo_palabras > len(lista_raices[0]): minimo_palabras = len(lista_raices[0])
        if maximo_palabras < len(lista_raices[0]): maximo_palabras = len(lista_raices[0])
        total_lista_raices_sinRepeticiones = total_lista_raices_sinRepeticiones + lista_raices[0]
        total_lista_raices.append(lista_raices[0])
        total_lista_raices_conRepeticiones = total_lista_raices_conRepeticiones + lista_raices[1]
    
    #Generar las 5 palabras de mayor frecuencia
    palabrasUnicas = []
    for w in total_lista_raices_conRepeticiones: #ELIMINAR LAS PALABRAS REPETIDAS EN OTRA LISTA
        if not w in palabrasUnicas:
            palabrasUnicas.append(w)
            
    frecuenciaPalab = []
    for w in palabrasUnicas: #CONTADOR DE CADA PALABRA (UNICA) DESDE LA LISTA QUE CONTIENE TODAS LAS PALABRAS (REPETIDAS)
        frecuenciaPalab.append(total_lista_raices_conRepeticiones.count(w))
    
    pair_palabras_frecuencia = list(zip(palabrasUnicas,frecuenciaPalab))
    pair_palabras_frecuencia = sorted(pair_palabras_frecuencia, key=itemgetter(1), reverse=True)
    
    palabras_mayorFrecuencia = []
    palabras_frecuenciaColeccion = []
    for i in range(5):
        palabras_frecuenciaColeccion.append(pair_palabras_frecuencia[i][1]/len(palabrasUnicas))
        palabras_mayorFrecuencia.append(pair_palabras_frecuencia[i])
    
    palabras5_mayorFrec = list(zip(palabras_mayorFrecuencia,palabras_frecuenciaColeccion))
    
    
    documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.3 --------------"+"\n")
    documentacion_final.write("El STEMMER empleado es PorterStemmer de la librería nltk.stem\n")
    documentacion_final.write("Número TOTAL de palabras ÚNICAS de la colección -> "+str(len(palabrasUnicas))+"\n")
    documentacion_final.write("Número MÍNIMO de palabras ÚNICAS una vez extraidas sus raices de los documentos en la colección-> "+str(minimo_palabras)+"\n")
    documentacion_final.write("Número MÁXIMO de palabras ÚNICAS una vez extraidas sus raices de los documentos en la colección-> "+str(maximo_palabras)+"\n")
    documentacion_final.write("Número MEDIO de palabras ÚNICAS de los documentos en la colección -> "+str(len(total_lista_raices_sinRepeticiones)/num_archivos)+"\n")
    documentacion_final.write("Las 5 palabras más frecuentes -> "+str(palabras5_mayorFrec)+"\n")
    
    #---------------------------------------------------------------------
    #EJECUCIÓN DE LA PRÁCTICA 1.4: CREACIÓN DE PARES PALABRA-FRECUENCIA.
    
    rutaColeccion = ruta_destino
    rutaDiccionario = config['OFFLINE']['ruta_almacen_palabras_frecuencia']
    pares_palabra_frecuencia = Pares_Palabra_Frecuencia()
    diccionario_palabras = pares_palabra_frecuencia.dicc_terminos(palabrasUnicas)
    dicc_palabras_invertido = pares_palabra_frecuencia.get_dicc_invert_terminos()
    diccionario_archivos = pares_palabra_frecuencia.dicc_ficheros(rutaColeccion)
    dicc_archivos_invertido = pares_palabra_frecuencia.get_dicc_invert_archivos()
    start_time = time.time()
    diccionarioPalabraFrec = pares_palabra_frecuencia.crearEEDD_palabrasFrecuencia(rutaColeccion)
    tiempo_ejecucion = time.time() - start_time
    tam_eedd = pares_palabra_frecuencia.guardarEEDD_palabrasFrecuencia(rutaDiccionario)
    diccionarioPalabraFrec = pares_palabra_frecuencia.cargarEEDD_palabrasFrecuencia(rutaDiccionario)
    
    rutaGuardado = config['OFFLINE']['ruta_diccionarios_invertidos']
    pares_palabra_frecuencia.guardarEEDD_diccPalabras_invertidas(rutaGuardado)
    pares_palabra_frecuencia.guardarEEDD_diccDocumentos_invertidas(rutaGuardado)
    rutaGuardado = config['OFFLINE']['ruta_diccionario_archivos']
    pares_palabra_frecuencia.guardarEEDD_diccArchivos(rutaGuardado)
    
    documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.4 --------------"+"\n")
    documentacion_final.write("Tiempo en segundos en calcular y generar la estructura de diccionario (la seleccionada) -> "+str(tiempo_ejecucion)+"\n")
    documentacion_final.write("El espacio en disco para guardar la estructura es de "+str(tam_eedd)+" bytes.\n")
    documentacion_final.write("Las caracteristicas de mi ordenador son:\n - Procesador: Inter(R) Core(TM) i7-8565U CPU @ 1.80GHz 1.99 GHz.\n - Memoria RAM: 7,82 GB utilizable.")
    
    
    #---------------------------------------------------------------------
    #EJECUCIÓN DE LA PRÁCTICA 1.5: Ficheros de pesos normalizados y no normalizados.
    
    #Se parte de los archivos últimos recogidos; es decir, los archivos a los que se les ha aplicado el Stemmer.
    rutaColeccion = config['OFFLINE']['ruta_coleccion_stemmer']
    contenido = os.listdir(rutaColeccion)
    ruta_destino = config['OFFLINE']['ruta_coleccion_ficherosNormalizados']
    archivos = [nombre for nombre in contenido if isfile(join(rutaColeccion,nombre))] #Obtener los archivos de la carpeta
    archivos_frecuencias_normalizadas = []
    fich_pesosNorm = Ficheros_Pesos_Normalizados()
    
    start_time = time.time()
    idf_palabrasUnicas = fich_pesosNorm.crear_IDF_palabras(diccionario_palabras,total_lista_raices, len(archivos))
    tiempo_ejecucion2 = time.time() - start_time
    
    
    start_time = time.time()
    pesos_palabras_documento = fich_pesosNorm.pesos_palabras_documento(rutaColeccion,idf_palabrasUnicas, diccionario_archivos, dicc_palabras_invertido)
    
    pesos_palabras_documento_norm = fich_pesosNorm.normalizar_pesos_documento(pesos_palabras_documento, dicc_archivos_invertido)
    tiempo_ejecucion1 = time.time() - start_time
    
    rutaGuardado = config['OFFLINE']['ruta_coleccion_ficherosNormalizados']
    tam_eedd_pesosNorm = fich_pesosNorm.guardarEEDD_pesosNorm(rutaGuardado, pesos_palabras_documento_norm)
    tam_eedd_IDF = fich_pesosNorm.guardarEEDD_IDF(rutaGuardado, idf_palabrasUnicas)
    
    dicc_pesosNorm = fich_pesosNorm.cargarEEDD_pesosNorm(rutaGuardado)
    dicc_IDF = fich_pesosNorm.cargarEEDD_IDF(rutaGuardado)
    
    
    documentacion_final.write("-------------- MEMORIA DE LA PRÁCTICA 1.5 --------------"+"\n")
    documentacion_final.write("Tiempo en segundos en calcular y generar la estructura de diccionario para los pesos normalizados (la seleccionada) -> "+str(tiempo_ejecucion1)+"\n")
    documentacion_final.write("Tiempo en segundos en calcular y generar la estructura de diccionario para los IDF (la seleccionada) -> "+str(tiempo_ejecucion2)+"\n")
    documentacion_final.write("El espacio en disco para guardar la estructura de pesos normalizados es de "+str(tam_eedd_pesosNorm)+" bytes.\n")
    documentacion_final.write("El espacio en disco para guardar la estructura de los IDF es de "+str(tam_eedd_IDF)+" bytes.\n")
    documentacion_final.write("Las caracteristicas de mi ordenador son:\n - Procesador: Inter(R) Core(TM) i7-8565U CPU @ 1.80GHz 1.99 GHz.\n - Memoria RAM: 7,82 GB utilizable.")
    documentacion_final.close() #CERRAR EL DOCUMENTO DE LA MEMORIA
    
#---------------------------------------------------------------------
#EJECUCIÓN DE LA PRÁCTICA 1.6: Ficheros de pesos normalizados y no normalizados.

fich_consultas = config['ONLINE']['ruta_fich_consultas']
num_doc_relevantes = config['ONLINE']['num_doc_relevantes']
num_doc_relevantes = int(num_doc_relevantes)
buscador = Buscador(config, fich_consultas, num_doc_relevantes)
buscador.procesar_pesos()


