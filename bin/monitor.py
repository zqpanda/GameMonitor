#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.extend(['../lib/','../conf/']) 
from crawl import WebCrawl2
from mlogger import *
from urls import *

def main():
    web_a=WebCrawl2()
    env=sys.argv[1]
    result=web_a.fetch_code_parallel(urls_list[env])
    print result
    

if __name__ == '__main__':
    main()
