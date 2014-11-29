#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,urllib2,chardet
import sys,time
import zlib 
sys.path.append('../conf/')
from mlogger import *



class WebCrawl2:
    def __init__(self):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 5.2; rv:7.0.1) Gecko/20100101 FireFox/7.0.1'
            }
    def url_read(self,url):
        '''
        页面内容抓取
        '''
        import httplib
        try:
            req=urllib2.Request(url, headers=self.headers)
            req.add_header('Accept-encoding', 'gzip')
            opener = urllib2.build_opener()
            response = opener.open(req)
            return response
        except urllib2.HTTPError,e:
            logging.error('HTTPError = ' + str(e.code))
            return None
        except urllib2.URLError,e:
            logging.error('URLError = ' + str(e.reason))
            return None
        except httplib.HTTPException,e:
            logging.error('HTTPException')
            return None
        except Exception:
            import traceback
            logging.error('generic exception: ' + traceback.format_exc())
            return None
    def url_parse(self,raw_url):
        from urlparse import urlparse
        url = urlparse(raw_url)
        url_info = {
                'hostname' : url.hostname,
                'port' : url.port,
                'path' : url.path,
                }
        return url_info

    def get_code(self,url):
        import httplib
        try:
            code = self.url_read(url).getcode()
            return code 
        except urllib2.HTTPError,e:
            return e.code
        except urllib2.URLError,e:
            return 333
        except httplib.HTTPException,e:
            return 444
        except Exception,e:
            import traceback
            logging.error('generic exception: ' + traceback.format_exc())
            return 666

    def content_crawl(self, url, try_times=3, sleep_time=0.2):
        '''
        重试机制，默认为3次且有sleep等待
        '''
        for i in range(try_times):
            response = self.url_read(url)
            if response != None:
                html = response.read()
                gzipped = response.headers.get('Content-Encoding')
                if gzipped:
                    html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
                encoding=chardet.detect(html)['encoding']
                if encoding == 'GB2312':
                    encoding = 'GBK'
                iconvcontent=html.decode(encoding)
                return iconvcontent
            else:
                time.sleep(sleep_time)
                continue
        logging.debug('Crawl Failed: %s' % url)
        return None

    def sync_parse(self, content, desc):
        pass

    def asyn_parse(self, content):
        #异步接口处理
        import simplejson
        result=simplejson.load(content)
        return result.keys()
    
    def code_crawl(self, url, try_times=3, sleep_time=0.2):
        #http code提取
        for i in range(try_times):
            code=self.get_code(url)
            if content == 200:
                return content
            else:
                time.sleep(sleep_time)
                continue
        logging.debug('Bad Url: %s' % url)
        return code

    def fetch_parallel(self, list_of_urls, pool_num=4):
        #并行抓取
        from multiprocessing.dummy import Pool as ThreadPool
        pool=ThreadPool(pool_num)
        results=pool.map(self.url_extract,list_of_urls)
        pool.close()
        pool.join()
        return results

    def url_extract(self, crawl_url, url_regex=''):
        #url提取
        from bs4 import BeautifulSoup
        from urlparse import urlparse
        scheme = urlparse(crawl_url).scheme
        hostname = urlparse(crawl_url).hostname
        complete_host = scheme + '://' + hostname + '/'
        web_content = self.content_crawl(crawl_url)
        soup = BeautifulSoup(web_content)
        all_links = soup.findAll('a')
        link_list = list()
        for link_item in all_links:
            if link_item.attrs.has_key('href'):
                raw_url = link_item.attrs['href'].strip('/ ')
                if urlparse(raw_url).hostname is not None:
                    link_list.append(raw_url)
                else:
                    link_list.append(complete_host + raw_url)
        return link_list


    def fetch_code_parallel(self,list_of_urls,pool_num=4):
        #并行获取http code
        from multiprocessing.dummy import Pool as ThreadPool
        pool=ThreadPool(pool_num)
        results=pool.map(self.get_code,list_of_urls)
        pool.close()
        pool.join()
        return results
        

def main():
    webcrawl=WebCrawl2()
   # print webcrawl.url_read(sys.argv[1])
    env=sys.argv[1]
    results=webcrawl.fetch_code_parallel(urls_list[env],12)
    #for url in urls:
    #    tmp=webcrawl.content_crawl(url)

if __name__ == '__main__':
    main()
