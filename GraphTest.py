import pymongo
import sys

# User credentials for DB
#http://www.seerinteractive.com/blog/visualize-your-backlinks-with-google-fusion-tables
#http://scicomp.stackexchange.com/questions/3315/visualizing-very-large-link-graphs
usr='crawlrdb'
pw='crawlrpw'
url='ds037407-a.mongolab.com'
port='37407'
dbname='madmaze-testdb'
colname='queueCol'

mongoURI='mongodb://'+usr+':'+pw+'@'+url+':'+port+'/'+dbname
print "connecting to db"
conn=pymongo.Connection(mongoURI)
db = conn[dbname]

print "getting db cursor"
dbCur = db[colname].find({"done":1},timeout=False)

allUrls={}

def findNode(label):
	if allUrls.has_key(label):
		N = g.nodes
		for n in N:
			if n.label==label:
				return n
	return None
	
cnt=0
f = open("/home/madmaze/Dropbox/Projects/crawlr/log.txt","a")
print "insering nodes.."
for url in dbCur:
	node = g.addNode()
	node.label=url['_id']
	allUrls[url['_id']]=1
	if cnt%10==0:
		print cnt
		f.write(str(cnt)+"\n")
	if url.has_key('urls'):
		for u in url['urls']:
			tmp = findNode(u)
			if tmp == None:
				subnode = g.addNode()
				subnode.label=u
				allUrls[u]=1
				edge = g.addDirectedEdge(node,subnode)
			else:
				edge = g.addDirectedEdge(node,tmp)
	cnt+=1
print "...done inserting"
f.close()
#	allUrls.append(url)
#
#
#for url in g.nodes:
#	if allUrls[url.label].has_key('urls'):
#		for u in allUrls[url.label]['urls']:
#			AllNodes = g.nodes
#			found=False
#			for n in AllNodes:
#				if n.label==u:
#					g.addEdge(url,n)
#			print u
			

# create nodes
#for i in range(50):
#	g.addNode()
 
# create edges randomly
#for u in g.nodes:
#	for v in g.nodes:
#		if random.random() < 0.5:
#			g.addEdge(u, v)
 
# run force atlas layout
print "running layout.."
run_layout(ForceAtlas, iters=100)
