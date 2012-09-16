#!/usr/bin/env python

import seed
import clientTools
import mongoConfig as mc

cT = clientTools.clientTools()
loopCnt=1
requestSize=5
skipCnt=0
while loopCnt<100:
    urls = cT.client("<request|"+requestSize+">")
    todoList = urls.strip('<>\n').split('|')
    #print todoList
    for todo in todoList:
        if todo != "":
            print "processing: ",todo
            s = seed.seed(url=todo,domain="tumblr.com",userAgent=mc.uA)
            if s.crawl() < 0:
                skipCnt+=1
    print "requests done:",(loopCnt*requestSize)
    print "skipCnt:",skipCnt