#!/usr/bin/env python

import socket
import threading
import SocketServer
import sys
import signal
import mongoConfig as mc
import mongoTools

server=""

#SocketServer.BaseRequestHandler
class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.mt = mongoTools.mongoTools(mc.usr,mc.pw,mc.url,mc.port,mc.dbname)
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        # http://blog.pythonisito.com/2012/01/getting-started-with-mongodb-and-python.html
        
    def handle(self):
        data = self.rfile.readline()
        self.addToQueue(data)
        cur_thread = threading.currentThread()
        response = "%s: %s" % (cur_thread.getName(), "got it")
        self.request.send(response)
    
    def addToQueue(self, data):
        print "adding items to queue..."
        fail=0
        x=0
        for packet in data.strip("\n").split(">|"):
            if len(packet)>0:
                bits = packet.strip().strip("<").strip(">").split("|")
                if bits[0] == "add":
                    res = self.mt.insertQueue(bits[1],int(bits[2]))
                    if res < 0:
                        print "issue inserting into database.."
                        fail+=1
                    x+=1
                elif bits[0] == "done":
                    res = self.mt.markDone(bits[1])
                    print bits[1]," marked done."
                else:
                    print "not yet implemented |",packet,"|"
                    
        print "Items added: %d/%d" % ((x-fail),x)
        

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    print "Received: %s" % response
    sock.close()

# catch signal to gracefully shut down
def signal_handler(signal, frame):
        print "shutting down.."
        server.shutdown()
        sys.exit(0)
    

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 65001

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # set the CTRL+C signal handler to exit gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    server_thread.start()
    print "Server loop running in thread:", server_thread.getName()
    
    signal.pause()
    