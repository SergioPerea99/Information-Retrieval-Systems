from xml.dom import minidom
from os.path import join

class Filtrado(object):

    # Constructor parametrizado
    def __init__(self, ruta):
        self.doc = minidom.parse(ruta)
        self.identificador = self.doc.getElementsByTagName("identifier")[0] #identificador del archivo
        self.fecha = self.doc.getElementsByTagName("dc:date")[0] #Fecha del documento
        self.nombre = self.doc.getElementsByTagName("dc:title")[0] #Nombre en español del documento
        self.fuente = self.doc.getElementsByTagName("dc:source")[0] #Fuente de donde proviene la información. Interesante a la hora de posicionar según la fuente.
        self.cuerpo = self.doc.getElementsByTagName("dc:description")[0]
        self.informacion = [self.nombre, self.fecha, self.fuente, self.cuerpo]

    #Método de normalización y tokenización
    def normalizacion_tokenizacion(self,ruta):
        aux = self.identificador.firstChild.data
        nombre_archivo = aux.split(":")
        no_borrar = ['-','_',' ']
        cadena = []
        num_tokens = 0
        archivo = open(join(ruta,nombre_archivo[len(nombre_archivo)-1]) +".txt","w")
        
        for i in self.informacion:
            aux = i.firstChild.data
            minus = aux.lower()
            for i in minus:
                if i.isalpha() or i.isdigit() or i in no_borrar:
                    cadena.append(i)
        
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
    
        


