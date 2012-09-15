crawlr
======

a web crawler with mongodb backend. This is a easily parallelizable system built in python.
The queueMaster hold the reigns to the database and communicated with any number of agents.

each agent polls the queueMaster for jobs to do(pages to parse) and then adds the discovered links back into the database by talking to the queueMaster