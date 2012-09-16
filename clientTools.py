#!/usr/bin/env python
'''
Created on Sep 15, 2012

@author: madmaze
'''
import socket
class clientTools:
    
    def __init__(self,host='',port=''):
        self.hostip = (host, socket.gethostbyname("localhost"))[host=='']
        self.port = (port, 65001)[port=='']

    def client(self, message, ip='', port=''):
        ip = (ip, self.hostip)[ip=='']
        port = (port, self.port)[port=='']
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(message+"\n")
        response = sock.recv(1024)
        
        sock.close()
        
        #print "Received: %s" % response
        return response