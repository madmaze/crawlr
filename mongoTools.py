#!/usr/bin/env python
'''
Created on Sep 9, 2012

@author: madmaze
'''
import pymongo
import mongoConfig

class mongoTools:
    def __init__(self,usr,pw,url,dbname):
        self.conn=pymongo.Connection(mongoConfig.mongourl)
        self.usr=usr
        self.pw=pw
        self.url=url
        self.dbname=dbname
        
    
    def insertQueue(self,url,cnt):
        db = self.conn['madmaze-testdb']
        res = db.madmaze_queue.find_one({"_id":url})
        if res == None:
            print "insert"
            db.madmaze_queue.insert({"_id":url, "cnt": cnt, "done": 0})
        else:
            err={'n':0}
            #refs:
            #http://www.mongodb.org/display/DOCS/Atomic+Operations#AtomicOperations-%22UpdateifCurrent%22
            #http://www.mongodb.org/display/DOCS/Updating#Updating-%7B%7Bupserts%7D%7D
            #http://api.mongodb.org/python/2.3/api/pymongo/collection.html#pymongo.collection.Collection.update
            while err['n'] != 1:
                orig = res['cnt']
                res['cnt'] += cnt
                err = db.madmaze_queue.update({"_id":url, "cnt": orig}, {"$set": {"cnt": res['cnt']} }, safe=True)
                print "added to it",res, orig
                if err['n']==0:
                    print "update failed..",err
                    res = db.madmaze_queue.find_one({"_id":url})
                else:
                    print "update successful"
             
        

mt = mongoTools("usr","pw","url","dbname")
mt.insertQueue("google.com/test2",1)
