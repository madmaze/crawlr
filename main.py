#!/usr/bin/env python

import seed
import clientTools
import mongoConfig as mc

cT = clientTools.clientTools()
loopCnt=1
requestSize=10
skipCnt=0
while loopCnt<100:
    urls = cT.client("<request|"+str(requestSize)+">")
    if "<none>" not in urls:
        todoList = urls.strip('<>\n').split('|')
        #print todoList
        for todo in todoList:
            if todo != "":
                print "processing: ",todo
                s = seed.seed(url=todo,domain="tumblr.com",userAgent=mc.uA)
                if s.crawl() < 0:
                    skipCnt+=1
        loopCnt+=1
    else:
        print "could not get new set of urls"
    print "requests done: %d / skipped: %d" % ((loopCnt*requestSize),skipCnt)