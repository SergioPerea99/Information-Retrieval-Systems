# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:18:34 2021

@author: Sergio Perea
"""

import cgi
# Headers
print("Content-Type: text/html")
print()
print("""<html>
    <head><title>SERGCHING</title></head>
    <form method="post" action="obtener_datos.py">
        <input name="name" type="text" /> <button>BUSCAR</button>  <br />
        
    </form>
</html>""")

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