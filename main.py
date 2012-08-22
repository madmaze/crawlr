#!/usr/bin/env python

import seed

s = seed.seed(url="http://taidaceli.tumblr.com",domain="tumblr.com",userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.77 Safari/537.1")

s.crawl()