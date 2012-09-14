#!/usr/bin/env python
#import sys
import urllib2
import socket
from HTMLParser import HTMLParser


class HTMLraper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []
	def handle_starttag(self, tag, attrs):
		#print "<",tag,">", attrs
		for k,v in attrs:
			if k == 'href':
				#print k, v
				self.data.append((k,v))
			elif 'http://' in v:
				#print k, v
				self.data.append((k,v))

	#def handle_endtag(self, tag):
		#print "<",tag,">"
		#sys.stdout.write(".")
	#def handle_data(self, data):
		#print "dat:",data
		#sys.stdout.write(".")

class seed:
	url=""
	domain=""
	userAgent=""
	depth=0
	newUrls={}
	HOST = "localhost"
	PORT = 65001
	
	def __init__(self,url='',domain="",userAgent='',depth=0):
		self.url = url
		self.domain = domain
		self.userAgent = userAgent
		self.depth = depth
		self.newUrls={}
	
	def client(self, ip, port, message):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
		sock.sendall(message+"\n")
		response = sock.recv(1024)
		print "Received: %s" % response
		sock.close()
	
	def crawl(self):
		headers = {'User-Agent' : self.userAgent}
		req = urllib2.Request(self.url,None,headers)
		resp = urllib2.urlopen(req)
		lines = resp.read().split("\n")
		parser = HTMLraper()
		for l in lines:
			#if l.find(self.domain) > 0:
			parser.feed(l)
		for k,v in parser.data:
			#print k,":",v
			if v[0]=="/":
				#print self.url+v
				if self.url+v in self.newUrls.keys():
					self.newUrls[self.url+v]+=1
				else:
					self.newUrls[self.url+v]=1
			elif v.find(self.domain)>=0:
				if v in self.newUrls.keys():
					self.newUrls[v]+=1
				else:
					self.newUrls[v]=1
				#print v
		for v in self.newUrls.keys():
			self.client(socket.gethostbyname(self.HOST), self.PORT, "<add|"+v+"|"+str(self.newUrls[v])+">")
			
			# submit to queue to processing