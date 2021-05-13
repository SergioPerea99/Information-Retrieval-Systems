# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:19:18 2021

@author: Sergio Perea
"""



import os
import cgi
import configparser
from buscador import Buscador
from os.path import join




# Headers
print("Content-Type: text/html")
print()
print("<html>")


print("""<style type="text/css">
  form {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

form input {
  width: 90%;
  height: 30px;
  margin: 0.5rem;
}

form button {
  padding: 0.5em 1em;
  border: none;
  background: rgb(100, 200, 255);
  cursor: pointer;
}
  </style>""")

print("""
    <head><title>SERGCHING</title></head>
    <form method="post" action="obtener_datos.py">
        <input name="name" type="text" /> <button>BUSCAR</button>  <br />
    </form>""")

buscador_input = cgi.FieldStorage()

if "name" not in buscador_input:
    print("<h1>NO HA ESCRITO NADA PARA BUSCAR.</h1>")
    print("<h2>POR FAVOR, ESCRIBA ALGO ANTES DE DAR AL BOTÓN DE BUSCAR.</h2>")
else:
    #TENEMOS LA FRASE, HAY QUE ESCRIBIR EN EL TEXTO DE LA CONSULTA.TXT Y LUEGO EJECUTAR LA PARTE ONLINE DEL SRI.
    
    config = configparser.ConfigParser()
    config.read('conf.ini')
    
    ruta_fichero_consultas = config['ONLINE']['ruta_fich_consultas']
    archivo = open(ruta_fichero_consultas,"w")
    archivo.write(str(buscador_input["name"].value)+"\n")
    archivo.close()
    
    buscador = Buscador(config,ruta_fichero_consultas,5)
    buscador.procesar_pesos()
    
    rutaColeccion = config['ONLINE']['ruta_ficheros_consultas_resultados_ordenados']
    contenido = os.listdir(rutaColeccion)
    
    archivos = [join(rutaColeccion,nombre) for nombre in contenido]
    
    for consulta in archivos:
        fichero = open(consulta,"r")
        for linea in fichero:
            print("<p>%s</p>" % (linea))
        fichero.close()
   
    

  
print("</html>")

