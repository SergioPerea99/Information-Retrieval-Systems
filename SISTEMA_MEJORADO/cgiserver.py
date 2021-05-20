# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:26:12 2021

@author: Sergio Perea
"""

from http.server import HTTPServer, CGIHTTPRequestHandler

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/"]
    
httpd = HTTPServer(("", 8050), Handler)
httpd.serve_forever()