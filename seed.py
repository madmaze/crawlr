#!/usr/bin/env python
import sys
import urllib2
from HTMLParser import HTMLParser


class HTMLraper(HTMLParser):
	def handle_starttag(self, tag, attrs):
		#print "<",tag,">", attrs
		for k,v in attrs:
			if k == 'href':
				print k, v
			elif 'http://' in v:
				print k, v
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
	
	def __init__(self,url='',domain="",userAgent='',depth=0):
		self.url = url
		self.domain = domain
		self.userAgent = userAgent
		self.depth = depth
	
	def crawl(self):
		headers = {'User-Agent' : self.userAgent}
		req = urllib2.Request(self.url,None,headers)
		resp = urllib2.urlopen(req)
		lines = resp.read().split("\n")
		parser = HTMLraper()
		for l in lines:
			#if l.find(self.domain) > 0:
			parser.feed(l)