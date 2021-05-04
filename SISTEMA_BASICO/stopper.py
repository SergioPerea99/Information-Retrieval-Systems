

class Stopper(object):

    #Constructor parametrizado
    def __init__(self,ruta):
        fichero = open(ruta,"r")
        self.contenido_fichero = []
        for linea in fichero:
            aniadir = linea.split("\n")
            self.contenido_fichero.append(aniadir[0])
        

    #Método para eliminar las palabras vacias de un archivo, almacenándolo en otro archivo dentro de la ruta indicada.
    def eliminacion_vacias(self,ruta_archivo, ruta_destino):
        fichero = open(ruta_archivo,"r")
        limpiar_vacias = []
        for linea in fichero:
            aniadir = linea.split("\n")
            if not aniadir[0] in self.contenido_fichero:
                limpiar_vacias.append(aniadir[0])
        fichero.close()
        
        archivo = open(ruta_destino,"w")
        for i in limpiar_vacias:
            archivo.write(i+"\n")
        archivo.close()
        return limpiar_vacias

        
        
            