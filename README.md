crawlr
======

a web crawler with mongodb backend. This is a easily parallelizable system built in python.
The queueMaster hold the reigns to the database and communicated with any number of agents.

each agent polls the queueMaster for jobs to do(pages to parse) and then adds the discovered links back into the database by talking to the queueMaster


License:
---
```
Copyright (c) 2012 Matthias Lee, matthias.a.lee[]gmail.com
Last edited: Sept 25th 2012

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```