#!/usr/bin/env python

import socket
import threading
import SocketServer
import sys
import signal
import mongoConfig as mc
import mongoTools
import singletonObj

queueLock = threading.Lock()
server=""
firstInst=singletonObj.singletonObj()

#SocketServer.BaseRequestHandler
class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.mt = mongoTools.mongoTools(mc.usr,mc.pw,mc.url,mc.port,mc.dbname)
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        # http://blog.pythonisito.com/2012/01/getting-started-with-mongodb-and-python.html
        
    def handle(self):
        data = self.rfile.readline()
        resp = self.manageQueue(data)
        self.request.send(resp)
    
    def manageQueue(self, data):
        fail=0
        x=0
        resp=""
        # TODO: make sure to save which urls linked to where
        if "<add|" in data or "<done|" in data:
            print "adding items to queue..."
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
                        
            resp = "Items added: %d/%d" % ((x-fail),x)
        elif "<request|" in data:
            # we are locking here to pass back and forth a singleton
            #    containing one instance of mongoTools so that when
            #    we are requesting TODOs, we can iterate over the
            #    cursor returned to us by the DB without loosing track
            #    of where we are.
            singleMongoTools=singletonObj.singletonObj()
            queueLock.acquire()
            try:
                
                bits = data.strip('<>\n').split("|")
                if bits[0] == "request":
                    print "processing request.."
                    resp = singleMongoTools.mt.requestURLs(int(bits[1]))
                else:
                    resp = "malformed packet: ",data
            finally:
                queueLock.release()
        else:
            resp = "malformed packet: ",data
            
        return resp
        

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
    