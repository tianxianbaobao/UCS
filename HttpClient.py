# -*- coding: utf-8 -*-
"""
Date     : 2015/09/25 20:21:56
FileName : HttpClient.py
Author   : septicmk
"""

import cookielib, urllib, urllib2, socket, urlparse
import os, sys

class HttpClient:
  __cookie = cookielib.CookieJar()
  __req = urllib2.build_opener(urllib2.HTTPCookieProcessor(__cookie))
  __req.addheaders = [
    #('Accept', 'application/javascript, */*;q=0.8'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    ('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
  ]
  urllib2.install_opener(__req)

  def Get(self, url, refer=None):
    try:
      req = urllib2.Request(url.replace(' ','%20'))
      if not (refer is None):
          req.add_header('Referer', refer)
      return urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
      return e.read()

  def Post(self, url, data, refer=None):
    try:
      req = urllib2.Request(url, urllib.urlencode(data))
      if not (refer is None):
        req.add_header('Referer', refer)
      return urllib2.urlopen(req, timeout=180).read()
    except urllib2.HTTPError, e:
      return e.read()

  def Download(self, url, file):
    print url
    def chunk_report(bytes_so_far, chunk_size, total_size):
      percent = int(bytes_so_far*100 / total_size)
      sys.stdout.write( "\r" + "Downloading" + '  ' + os.path.basename(file) + " ...(%.1f KB/%.1f KB)[%d%%]" % (bytes_so_far/1024.0, total_size/1024.0, percent))
      sys.stdout.flush()

      if bytes_so_far >= total_size:
         sys.stdout.write('\n')
         sys.stdout.flush()

    def chunk_read(response, chunk_size=8192, report_hook=None):
      try:
       total_size = response.info().getheader('Content-Length').strip()
      except:
       return response.read()
       total_size = int(total_size)
       bytes_so_far = 0
       ret = ''
    
       while 1:
          chunk = response.read(chunk_size)
          bytes_so_far += len(chunk)
          ret += chunk
    
          if not chunk:
             break
    
          if report_hook:
             report_hook(bytes_so_far, chunk_size, total_size)
    
       return ret

    output = open(file, 'wb')
    try:
        response = urllib2.urlopen(url)
        content = chunk_read(response, report_hook=chunk_report)
        output.write(content)
    except:
        parsed_link = urlparse.urlsplit(url.encode('utf8'))
        parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
        url = parsed_link.geturl()
        response = urllib2.urlopen(url)
        content = chunk_read(response, report_hook=chunk_report)
        output.write(content)

    output.close()

#  def urlencode(self, data):
#    return urllib.quote(data)

  def getCookie(self, key):
    for c in self.__cookie:
      if c.name == key:
        return c.value
    return ''

  def setCookie(self, key, val, domain):
    ck = cookielib.Cookie(version=0, name=key, value=val, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    self.__cookie.set_cookie(ck)
#self.__cookie.clear() clean cookie
