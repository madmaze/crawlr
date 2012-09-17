#!/usr/bin/env python
'''
Created on Sep 9, 2012

@author: madmaze
'''
import pymongo

class mongoTools:
    def __init__(self,usr,pw,url,port,dbname):
        mongoURI='mongodb://'+usr+':'+pw+'@'+url+':'+port+'/'+dbname
        #print "Init mongoDB connection"
        self.conn=pymongo.Connection(mongoURI)
        self.usr=usr
        self.pw=pw
        self.url=url
        self.port=port
        self.queueCol='queueCol'
        self.dbname=dbname
        self.todoCursor=None
        
    
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

    def markDone(self,url,linkList={}):
        db = self.conn[self.dbname]
        res = db[self.queueCol].find_one({"_id":url})
        links=""
        if len(linkList) > 0:
            for n,link in enumerate(linkList):
                if n!= 0:
                    links+=',"'+link+'"'
                else:
                    links+='"'+link+'"'
        if res == None:
            if len(linkList) > 0:
                res = db[self.queueCol].insert({"_id":url, "cnt": 0, "done": 1, "urls": linkList},safe=True)
            else:
                res = db[self.queueCol].insert({"_id":url, "cnt": 0, "done": 1},safe=True)
            print "marking done by inserting new", res
            if res['n']==0:
                    print "insert failed..",res
                    return -1            
        else:
            if len(linkList) > 0:
                res = db[self.queueCol].update({"_id":url, "done": 0}, {"$set": {"done": 1, "urls": linkList} },safe=True)
            else:
                res = db[self.queueCol].update({"_id":url, "done": 0}, {"$set": {"done": 1} },safe=True)
            if res['n']==0:
                    print "update failed..",res
                    return -1
        return 0
    
    # grab the shared database cursor to non-crawled urls.
    #    if none exist or we have come to an end, grab a new one
    #    then return as many urls as are available
    def requestURLs(self,cnt):
        db = self.conn[self.dbname]
        try:
            if self.todoCursor == None or self.todoCursor.alive == False:
                self.todoCursor = db[self.queueCol].find({"done":0},timeout=False)
                # check is anything was left/is found else return none
                if self.todoCursor.alive != True:
                    return '<none>'
            packet="<" 
            for i in range(cnt):
                if self.todoCursor.alive:
                    res = self.todoCursor.next()
                    packet+=res['_id']+"|"
            
            packet+=">"
            return packet
        except pymongo.errors.OperationFailure, e:
            print "Error in requestURLs:",e.code
        except:
            print "Error in requestURLs"
        return "<none>"

