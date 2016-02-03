#!/usr/bin/env python
import os
import imp
import sys

#
# Below for testing only
#
if __name__ == '__main__':
    ip   = 'localhost'
    port = 8051
    print 'Listening on http://localhost:8051'
    zapp = imp.load_source('application', 'wsgi/application')

    from wsgiref.simple_server import make_server
    httpd = make_server(ip, port, zapp.application)
    httpd.serve_forever()
