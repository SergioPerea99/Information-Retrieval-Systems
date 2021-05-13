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
        <input name="name" type="text" /> <br />
        <button>BUSCAR</button>
    </form>
</html>""")