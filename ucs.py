# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:09:45 2015

@author: freeman
"""

#import urllib2

#url = "http://sep.ucas.ac.cn/userName=zhangzhengyu%40ncic.ac.cn&pwd=espider&sb=sb"
#req = urllib2.Request(url)
#con = urllib2.urlopen( req )
#doc = con.read()
#print doc
#con.close()
#print 'DONE'

#!/usr/bin/python  
  
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
  
#登录的主页面  
hosturl = 'http://sep.ucas.ac.cn' #自己填写  
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://sep.ucas.ac.cn/slogin' #从数据包中分析出，处理post请求的url  
  
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
h = urllib2.urlopen(hosturl)  
  
#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
           'Referer' : '******'}  
#构造Post数据，他也是从抓大的包里分析得出的。  
postData = {'userName':'zhangzhengyu@ncic.ac.cn',
            'pwd':'espider',
            'sb':'sb'}  
  
#需要给Post数据编码  
postData = urllib.urlencode(postData)  
  
#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
request = urllib2.Request(posturl, postData, headers)  
response = urllib2.urlopen(request)  
text = response.read()  

#抓SEP APPSTORE里的“课程主页”
course_index = 'http://sep.ucas.ac.cn/portal/site/16/801'
response = urllib2.urlopen(course_index)
text = response.read()

course_index = 'http://course.ucas.ac.cn/portal?sakai.session=f180fd55-3420-473c-bdee-e30f02e4cc05&_mid=3c57988d-0d80-4925-bc4e-e7e6dda60acb'
response = urllib2.urlopen(course_index)
text = response.read()

#每个课程的主页入口
course_urls = re.findall(r'http://course.ucas.ac.cn/portal/site/\d+', text)
print course_urls

#下面被注释的代码用于遍历课程入口，进入课程主页寻找资源。
#for course_url in course_urls:
#   response = urllib2.urlopen(course_url)
#   text = response.read()
#   resourse_url = re.findall(r'http://course.ucas.ac.cn/portal/site/117020/page/.*',text)[2][0:-3]
#但是我们不需要这样做。我们需要从每个课程的主页入口获得课程代码，然后用下面的方式查找资源：
#   http://course.ucas.ac.cn/access/content/group/+课程代码

for course_url in course_urls:
    courseid = re.findall(r'http://course.ucas.ac.cn/\d+', course_url)