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


print("""<div class="container">
  <header class="header">
    <h1 id="title" class="text-center">COLECCIÓN SciELO.</h1>
    <p id="description" class="description text-center">
      REVISTAS CIENTÍFICAS ESPAÑOLAS DE CIENCIAS DE LA SALUD.
    </p>
  </header>
  <form id="survey-form" method="post" action="obtener_datos.py" accept-charset="UTF-8">
    <div class="form-group">
      <label id="name-label" for="name"></label>
      <input
        type="text"
        name="name"
        id="name"
        class="form-control"
        placeholder="Introduzca aquí su consulta..."
        required
      />
    </div>
  </form>
</div>""")

print("""<style type="text/css">
      :root {
  --color-white: #f3f3f3;
  --color-aqua: #00FFFF;
  --color-fuchsia: rgba(255,0,255, 0.8);
  --color-teal: #008080;
  --color-dark: #000000;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
  color: var(--color-white);
  margin: 0;
}

body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -1;
  background: var(--color-white);
  background-image: linear-gradient(
      100deg,
      rgba(0,255,255, 0.8),
      rgba(136, 136, 206, 0.7)
    ),
    url(https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.freepik.com%2Fvector-gratis%2Fcirculo-neon-efecto-luz-puntos-sobre-fondo-negro_106065-12.jpg&f=1&nofb=1);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

h1 {
  font-weight: 400;
  line-height: 1.2;
}

p {
  font-size: 1.125rem;
}

h1,
p {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

label {
  display: flex;
  align-items: center;
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

input,
button,
select,
textarea {
  margin: 0;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

button {
  border: none;
}

.container {
  width: 100%;
  margin: 3.125rem auto 0 auto;
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

.header {
  padding: 0 0.625rem;
  margin-bottom: 1.875rem;
}

.description {
  font-style: italic;
  font-weight: 200;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.4);
}

.clue {
  margin-left: 0.25rem;
  font-size: 0.9rem;
  color: #e4e4e4;
}

.text-center {
  text-align: center;
}

/* form */

form {
  background: var(--color-fuchsia);
  padding: 2.5rem 0.625rem;
  border-radius: 0.25rem;
}

@media (min-width: 480px) {
  form {
    padding: 2.5rem;
  }
}

.form-group {
  margin: 0 auto 1.25rem auto;
  padding: 0.25rem;
}

.form-result {
  background: var(--color-);
  padding: 2.5rem 0.625rem;
  border-radius: 0.25rem;
}

.form-result {
  background: var(--color-dark);
  padding: 2.5rem 0.625rem;
  border-radius: 0.25rem;
}

.form-control {
  display: block;
  width: 100%;
  height: 2.375rem;
  padding: 0.375rem 0.75rem;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.input-radio,
.input-checkbox {
  display: inline-block;
  margin-right: 0.625rem;
  min-height: 1.25rem;
  min-width: 1.25rem;
}

.input-textarea {
  min-height: 120px;
  width: 100%;
  padding: 0.625rem;
  resize: vertical;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background: var(--color-teal);
  color: inherit;
  border-radius: 2px;
  cursor: pointer;
}

</style>""")




buscador_input = cgi.FieldStorage()

if "name" in buscador_input:
    #TENIENDO LA FRASE, HAY QUE ESCRIBIR EN EL TEXTO DE LA CONSULTA.TXT Y LUEGO EJECUTAR LA PARTE ONLINE DEL SRI.
    config = configparser.ConfigParser()
    config.read('conf.ini')
    
    ruta_fichero_consultas = config['ONLINE']['ruta_fich_consultas']
    archivo = open(ruta_fichero_consultas,"w", encoding='utf8')
    archivo.write(str(buscador_input["name"].value)+"\n")
    archivo.close()
    
    buscador = Buscador(config,ruta_fichero_consultas,5)
    buscador.procesar_pesos()
    
    rutaColeccion = config['ONLINE']['ruta_ficheros_consultas_resultados_ordenados']
    contenido = os.listdir(rutaColeccion)
    
    archivos = [join(rutaColeccion,nombre) for nombre in contenido]
    
    
    
    for consulta in archivos:
        fichero = open(consulta,"r")
        i = 0
        
        for linea in fichero:
            if i == 0:
                print("""<div class="container">
                      <form id="survey-form">
                      <div class="form-group">
                      <p id="description" class="description text-center">%s</p>
                      </div>        
                      </form>
                      </div>""" % (linea))
            else:
                
                if (i-1)%3 == 0:
                    print("""<div class="container">
                          <form id="survey-form">
                          <div class="form-result">
                          <a class="text-center" href = "%s"> """ % (linea))
                
                if (i-1)%3 == 1:
                    print("""<h1>%s</h1></a>"""  % (linea))
                
                if (i-1)%3 == 2:
                    #Cuerpo del documento... 
                    #Se va a mostrar la parte con mayor relevancia según la consulta
                    pesosPalabrasConsulta = buscador.getPesosPalabrasConsulta()
                    #(str(pesosPalabrasConsulta))
                    
                    #PROBLEMA: LA PALABRA VIENE YA CON EL STEMMER HECHO !!!
                    #SOLUCIÓN: HACER COMPROBACIÓN DE SI LA CADENA DE CARACTERES ES LA MISMA A LA QUE HAYA EN LA LISTA (CUERPO DE TODO EL DOC).
                    
                    lista_contenido = linea.split(" ")
                    #print(lista_contenido)
                    
                    lista_posiciones_palabra = []
                    
                    for palabra_peso in pesosPalabrasConsulta:
                        contador = 0
                        for p in lista_contenido:
                            if palabra_peso[0] in p: #Si encuentra la subcadena (por el stemmer)
                                lista_posiciones_palabra.append((palabra_peso[0],contador)) #Añadir un sitio que nos localiza la palabra-posición donde aparece del documento
                            contador += 1
                    
                    #YA TENGO LA LISTA DE PALABRAS Y SUS POSICIONES EN EL TEXTO, AHORA UNA HEURÍSTICA POR CERCANÍA.
                    #Heurística básica --> ordenación por número, encontrar los distintos términos más próximos...
                    lista_posiciones_palabra = sorted(lista_posiciones_palabra, key=lambda palabraPeso : palabraPeso[1])
                    
                    j = 0
                    min_distancias = 10000
                    pos_solucion = -1
                    while(j < len(lista_posiciones_palabra)-1):
                        if lista_posiciones_palabra[j][0] not in lista_posiciones_palabra[j+1][0]: #Encuentra 2 términos distintos...
                            dif =  lista_posiciones_palabra[j+1][1] - lista_posiciones_palabra[j][1]
                            if dif < min_distancias: #Encontrar 2 términos distintos a la menor distancia posible...
                                pos_solucion = lista_posiciones_palabra[j][1] #Nos quedamos con la posición más baja que será la que va antes del posterior término diferente
                                min_distancias = dif
                            
                        j += 1
                    
                    if pos_solucion == -1: #En caso de no haber encontrado 2 términos distintos, añadir la posición de la primera palabra encontrada.
                        pos_solucion = lista_posiciones_palabra[0][1] 
                    
                    #print(pesosPalabrasConsulta)
                    #print(pos_solucion)
                    
                    #AHORA, MOSTRAR EL CONTENIDO ENTRE UN INTERVALO DONDE LA MITAD SEA EL POS_SOLUCION...
                    palabras_negrita = {contenido[0]: "" for contenido in pesosPalabrasConsulta}
                    poss = pos_solucion - 10
                    if poss < 0: 
                        poss = 0 
                    max_pos = pos_solucion + 10
                    if max_pos >= len(lista_contenido):
                        max_pos = len(lista_contenido)-1
                    
                    print("""<p class="text-center">...""")
                    while poss < max_pos:
                        negrita = False
                        for pal_negrita in palabras_negrita:
                            if pal_negrita in lista_contenido[poss]:
                                negrita = True
                                print("""<b>%s </b>""" % (lista_contenido[poss])) 
                        if not negrita:
                            print("""%s """ % (lista_contenido[poss]))
                        poss += 1
                    print("""...</p></div></form></div>)""")
            i += 1
        fichero.close()
   
print("</html>")

