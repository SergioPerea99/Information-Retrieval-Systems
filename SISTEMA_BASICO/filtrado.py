from xml.dom import minidom
from os.path import join
import re

class Filtrado(object):

    # Constructor parametrizado
    def __init__(self, ruta):
        extension = ruta.split(".")
        self.doc_xml = False
        if extension[len(extension)-1] == 'xml':
            self.doc = minidom.parse(ruta)
            self.identificador = self.doc.getElementsByTagName("identifier")[0] #identificador del archivo
            self.fecha = self.doc.getElementsByTagName("dc:date")[0] #Fecha del documento
            self.nombre = self.doc.getElementsByTagName("dc:title")[0] #Nombre en español del documento
            self.fuente = self.doc.getElementsByTagName("dc:source")[0] #Fuente de donde proviene la información. Interesante a la hora de posicionar según la fuente.
            self.cuerpo = self.doc.getElementsByTagName("dc:description")[0]
            self.informacion = [self.nombre, self.fecha, self.fuente, self.cuerpo]
            self.doc_xml = True
        elif extension[len(extension)-1] == 'txt':
            archivo = open(ruta,"r")
            self.informacion = []
            for linea in archivo:
                self.informacion.append(linea)
        else:
            print("NO ES NINGUNO DE LOS FORMATOS PROCESABLES")

    #Método de normalización y tokenización para archivos xml y txt
    def normalizacion_tokenizacion(self,ruta):
        if self.doc_xml:
            aux = self.identificador.firstChild.data
            nombre_archivo = aux.split(":")
            archivo = open(join(ruta,nombre_archivo[len(nombre_archivo)-1]) +".txt","w")
        else:
            archivo = open(ruta,"w")
            
        no_borrar = ['-','_',' ']
        cadena = []
        num_tokens = 0
        
        cont = 0
        for i in self.informacion:
            aux = i
            if self.doc_xml:
                aux = i.firstChild.data
            minus = aux.lower()
            cont = cont + 1
            for i in minus:
                if i.isalpha() or i.isdigit() or i in no_borrar:
                    cadena.append(i)
            if cont < len(self.informacion):
                if self.doc_xml:
                    cadena.append("\n")
                else:
                    cadena.append(" ")
        
        lista_palabras = ''.join(cadena)
        lista_palabras = lista_palabras.split(" ")
        
        i = 0
        while i < len(lista_palabras):
            if lista_palabras[i] != '':
                archivo.write(lista_palabras[i])
                num_tokens += 1
                if not i == len(lista_palabras)-1:
                    archivo.write("\n")
            i += 1
        archivo.close()
        devolver = (num_tokens,lista_palabras)
        return devolver
    
    

