from xml.dom import minidom


class Filtrado(object):
    informacion = []
    # Constructor parametrizado
    def __init__(self, ruta):
        self.doc = minidom.parse(ruta)
        self.fecha = self.doc.getElementsByTagName("dc:date")[0] #Fecha del documento
        self.nombre = self.doc.getElementsByTagName("dc:title")[0] #Nombre en español del documento
        
        #self.autores = doc.getElementsByTagName("dc:creator") #Contenedor de autores
        #self.temas = doc.getElementsByTagName("dc:subject") #Temas relacionados con el documento
        self.fuente = self.doc.getElementsByTagName("dc:source")[0] #Fuente de donde proviene la información. Interesante a la hora de posicionar según la fuente.
        print(self.nombre.firstChild.data)
        print(self.fecha.firstChild.data, " :: ", self.fuente.firstChild.data)
        self.cuerpo = self.doc.getElementsByTagName("dc:description")[0]
        self.informacion = [self.nombre, self.fecha, self.fuente, self.cuerpo]


    def normalizacion(self):
        archivo = open('C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\prueba.txt','w')
        a = ""
        for i in self.informacion:
            aux = i.firstChild.data
            minus = aux.lower()
            espacio = " "
            a = minus.split(espacio)
            archivo.write(''.join([i+"\n" for i in a if i.isalpha()]))
        archivo.close()
        

filtro = Filtrado("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021\S0211-69952009000500006.xml")
filtro.normalizacion()
