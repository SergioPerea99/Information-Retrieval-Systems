from xml.dom import minidom


class Filtrado(object):
    informacion = []
    # Constructor parametrizado
    def __init__(self, ruta):
        doc = minidom.parse(ruta)
        fecha = doc.getElementsByTagName("dc:date")[0] #Fecha del documento
        nombre = doc.getElementsByTagName("dc:title")[0] #Nombre en español del documento
        
        autores = doc.getElementsByTagName("dc:creator") #Contenedor de autores
        temas = doc.getElementsByTagName("dc:subject") #Temas relacionados con el documento
        fuente = doc.getElementsByTagName("dc:source")[0] #Fuente de donde proviene la información. Interesante a la hora de posicionar según la fuente.
        print(nombre.firstChild.data)
        print(fecha.firstChild.data, " :: ", fuente.firstChild.data)
        cuerpo = doc.getElementsByTagName("dc:description")[0]


    

filtro = Filtrado("C:\CODIGO\SRI\PRACTICAS_SRI\SISTEMA_BASICO\Colección_SRI_2021\S0211-69952009000500006.xml")

