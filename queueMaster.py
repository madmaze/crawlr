#!/usr/bin/env python
#import sys
import socket
import threading
import SocketServer
import os
import time
import pymongo

#SocketServer.BaseRequestHandler
class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        self.dbconn = pymongo.Connection('mongodb://crawlrdb:crawlrpw@ds037407.mongolab.com:37407/madmaze-testdb')
        self.queue = self.dbconn['madmaze-queue']
        self.finaldb = self.dbconn['madmaze-finaldb']
        # db.test_collection.insert({'inurl':'http://google.com/x','outurl':['fb','g+','other']})
        # http://blog.pythonisito.com/2012/01/getting-started-with-mongodb-and-python.html
        
    def handle(self):
        data = self.rfile.readline()
        self.addToQueue(data)
        #data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        response = "%s: %s" % (cur_thread.getName(), "got it")
        self.request.send(response)
    
    def addToQueue(self, data):
        bits = data.strip().strip("<").strip(">").split("|")
        if bits[0] == "add":
            print "adding:", bits[1]
            print "\tcount:", bits[2]
        else:
            print "not yet implemented"
        

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    print "Received: %s" % response
    sock.close()
    

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 65001

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    #server_thread.setDaemon(True)
    server_thread.start()
    print "Server loop running in thread:", server_thread.getName()

    #for i in range (0,1000):
    #    client(ip, port, "Hello World"+str(i))
    while os.path.isfile(".go"):
        time.sleep(10)
        print "found \".go\" to kill 'rm .go'.."
    
    print "shutting down.."
    server.shutdown()
