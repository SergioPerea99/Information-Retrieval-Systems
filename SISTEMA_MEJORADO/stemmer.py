from nltk.stem import PorterStemmer

class Stemmer(object):
    def extraccion_raices(self,ruta_archivo, ruta_destino):
        fichero = open(ruta_archivo,"r")
        lista_palabras = []
        for linea in fichero:
            lista_palabras.append(linea)
        fichero.close()
        
        archivo = open(ruta_destino,"w")
        porter = PorterStemmer()
        sinRepeticiones = []
        conRepeticiones =  []
        for w in lista_palabras:
           w = w.replace("\n","")
           w = porter.stem(w)
           archivo.write(w+"\n")
           if not w in sinRepeticiones:
               sinRepeticiones.append(w)
           conRepeticiones.append(w)
        archivo.close()
        devolver = [sinRepeticiones, conRepeticiones]
        return devolver