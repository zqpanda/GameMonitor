'''
import chardet,zlib
import chardet,gzip,StringIO
import urllib2

request = urllib2.Request('http://www.sohu.com')
request.add_header('Accept-encoding','gzip')
opener = urllib2.build_opener()
response = opener.open(request)
html = response.read()
gzipped = response.headers.get('Content-Encoding')
if gzipped:
    html = zlib.decompress(html, 16+zlib.MAX_WBITS)
encoding = chardet.detect(html)['encoding']
print html.decode(encoding).encode('utf-8')
content = urllib2.urlopen('http://www.sina.com.cn')
html = content.read()
print StringIO.StringIO(html)
page_content = gzip.GzipFile(fileobj=StringIO.StringIO(html), mode="r")
encoding = chardet.detect(page_content)['encoding']
print encoding
'''
import urllib2
import gzip, cStringIO

html = urllib2.urlopen('http://blog.raphaelzhang.com').read()
if html[:6] == '\x1f\x8b\x08\x00\x00\x00':
      html = gzip.GzipFile(fileobj = cStringIO.StringIO(html)).read()
print html
