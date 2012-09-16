#!/usr/bin/env python
'''
Created on Sep 9, 2012

@author: madmaze
'''
import pymongo

class mongoTools:
    def __init__(self,usr,pw,url,port,dbname):
        mongoURI='mongodb://'+usr+':'+pw+'@'+url+':'+port+'/'+dbname
        print "Init mongoDB connection"
        self.conn=pymongo.Connection(mongoURI)
        self.usr=usr
        self.pw=pw
        self.url=url
        self.port=port
        self.queueCol='queueCol'
        self.dbname=dbname
        
    
    def insertQueue(self,url,cnt):
        db = self.conn[self.dbname]
        res = db[self.queueCol].find_one({"_id":url})
        if res == None:
            #print "insert"
            db[self.queueCol].insert({"_id":url, "cnt": cnt, "done": 0})
            return 0
        else:
            err={'n':0}
            failCnt=0
            #refs:
            #http://www.mongodb.org/display/DOCS/Atomic+Operations#AtomicOperations-%22UpdateifCurrent%22
            #http://www.mongodb.org/display/DOCS/Updating#Updating-%7B%7Bupserts%7D%7D
            #http://api.mongodb.org/python/2.3/api/pymongo/collection.html#pymongo.collection.Collection.update
            while err['n'] != 1 and failCnt<10:
                orig = res['cnt']
                res['cnt'] = int(res['cnt']) + cnt
                err = db[self.queueCol].update({"_id":url, "cnt": orig}, {"$set": {"cnt": res['cnt']} }, safe=True)
                #print "added to it",res, orig
                if err['n']==0:
                    print "update failed..",err
                    res = db[self.queueCol].find_one({"_id":url})
                    failCnt+=1
                #else:
                    #print "update successful"
            if failCnt >= 10:
                print "failCnt above 10.. are we locked? did we loose connection?"
                return -1
            return 0

    def markDone(self,url):
        db = self.conn[self.dbname]
        res = db[self.queueCol].find_one({"_id":url})
        if res == None:
            #print "insert"
            db[self.queueCol].insert({"_id":url, "cnt": 0, "done": 1})
        else:
            db[self.queueCol].madmaze_queue.update({"_id":url, "done": 0}, {"$set": {"done": 1} })

