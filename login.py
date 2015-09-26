# -*- coding: utf-8 -*-
"""
Date     : 2015/09/25 20:21:53
FileName : login.py
Author   : septicmk
"""

from HttpClient import *
import re
import logging
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(
    filename='UCS.log',
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)

def check_existed(path):
    import os
    return os.path.exists(path)

def get_revalue(html, rex, er, ex):
    v = re.search(rex, html)
    if v is None:
        if ex:
            logging.error(er)
            raise TypeError(er)
        else:
            logging.warning(er)
        return ''
    return v.group(1)

class Course:

    def __init__(self):
        self.hosturl = 'http://sep.ucas.ac.cn'
        self.loginurl = 'http://sep.ucas.ac.cn/slogin'
        self.req = HttpClient()
	config = ConfigParser.ConfigParser()
	config.read('./ucs.config')
	self.usrname =  config.get('USER','usrname')
        self.passwd = config.get('USER', 'passwd')
        self.pwd = config.get('USER', 'savedir')

    def login(self):

        self.req.Get(self.hosturl)
        postData = {'userName': self.usrname,
                    'pwd': self.passwd,
                    'sb':'sb'}
        html = self.req.Post(self.loginurl, postData)
        logging.info('login success')

        course_index = 'http://sep.ucas.ac.cn/portal/site/16'
        html = self.req.Get(course_index) 

        Identity= get_revalue(html, r'Identity=(.+?)"', 'get Identity error', 1)
        logging.debug("Identity=" + Identity)

        html = self.req.Get("http://course.ucas.ac.cn/portal/plogin?Identity={0}".format(Identity) )
        session = get_revalue(html, r'session=(.+?)&', 'get session error', 1)
        _mid = get_revalue(html, r'_mid=(.+?)"', 'get mid error', 1)
        guid = get_revalue(html, r'guid=(.+?)"', 'get guid error', 1)
        logging.debug("session=" + session)
        logging.debug("_mid=" + _mid)
        logging.debug("guid=" + guid)

        html = self.req.Get("http://course.ucas.ac.cn/portal?sakai.session={0}&_mid={1}".format(session, _mid))
        course_urls = re.findall(r'http://course.ucas.ac.cn/portal/site/\d+', html)
        #return course_urls
        for test_url in course_urls:
            self.get_resource(test_url)


    def get_resource(self, url):
        import HTMLParser

        html_parser = HTMLParser.HTMLParser()
        html = self.req.Get(url)
        res_url = get_revalue(html, r'class="icon-sakai-resources" href="(.+?)"', 'get resource error', 1)
        logging.debug("res_url= "+res_url)
        html = self.req.Get(res_url)
        wtf_url = get_revalue(html, r'http://course.ucas.ac.cn/portal/tool-reset/(.+?)/', 'what the fuxk error', 1)
        html = self.req.Get("http://course.ucas.ac.cn/portal/tool-reset/{0}/?panel=Main".format(wtf_url))
        html = html_parser.unescape(html)
        #logging.debug(html)

        title = get_revalue(html, r'<img src =.*?/>([\s\S]+?)</h3>', 'get title error', 1).strip().replace(' ','_')
        logging.debug(title)
        res = re.findall(r'http://course.ucas.ac.cn/access/content/group/[^"]+', html)
        res = list(set(res))
        self.download(title, res)
        logging.debug(str(res))
    
    def download(self, title, res):
        import os
        print 'linking... ' + title
        logging.info('linking... ' + title)
        if not os.path.exists(self.pwd):
            os.makedirs(self.pwd)
        _pwd = os.path.join(self.pwd, title)
        if not os.path.exists(_pwd):
            os.makedirs(_pwd)
        for f in res:
            name = get_revalue(f, r'([^/]+?)$', 'get name error', 1).replace(' ', '_')
            __pwd = os.path.join(_pwd, name)
            if check_existed(__pwd):
                logging.info( name + ' already exists, skip')
                continue
            print 'downloading ' + name
            logging.info('downloading ' + name)
            self.req.Download(f, __pwd)

if __name__ == '__main__':
    c = Course()
    c.login()



