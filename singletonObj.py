'''
Created on Sep 15, 2012

@author: madmaze
REF: http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
'''
import mongoTools
import mongoConfig as mc

class singletonObj(object):
    _instance = None
    mt = ""
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(singletonObj, cls).__new__(cls, *args, **kwargs)
            # only initialized mongoTools once to preserve the DB cursor
            cls.mt = mongoTools.mongoTools(mc.usr,mc.pw,mc.url,mc.port,mc.dbname)
        return cls._instance

            