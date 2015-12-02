# coding=utf-8

import urllib2
import urllib
import cookielib
import sys
import re
import lxml.html as HTML
import socket

class Fetcher(object):
    def __init__(self, username=None, pwd=None, cookie_filename=None):
        #获取一个保存cookie的对象
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        #创建一个opener,将保存了cookie的http处理器，还有设置一个handler用于处理http的url的打开
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起
        urllib2.install_opener(self.opener)

        self.username = username
        self.pwd = pwd
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Referer':'','Content-Type':'application/x-www-form-urlencoded'}

    def get_rand(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}
        req = urllib2.Request(url ,"", headers)
        login_page = urllib2.urlopen(req).read()
        rand = HTML.fromstring(login_page).xpath("//form/@action")[0]
        passwd = HTML.fromstring(login_page).xpath("//input[@type='password']/@name")[0]
        vk = HTML.fromstring(login_page).xpath("//input[@name='vk']/@value")[0]
        return rand, passwd, vk

    def login(self, username=None, pwd=None, cookie_filename=None):
        if self.username is None or self.pwd is None:
            self.username = username
            self.pwd = pwd
        assert self.username is not None and self.pwd is not None

        url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dhome%26rl%3D1&backTitle=%CE%A2%B2%A9&vt=4'
        #获取随机数rand、password的name和vk
        rand, passwd, vk = self.get_rand(url)
        data = urllib.urlencode({'mobile': self.username,
                                 passwd: self.pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': '新浪微博',
                                 'vk': vk,
                                 'submit': '登录',
                                 'encoding': 'utf-8'})
        url = 'http://login.weibo.cn/login/' + rand

        #提交模拟登录
        page =self.fetch(url,data)
        #link = HTML.fromstring(page).xpath("//a/@href")[0]
        #if not link.startswith('http://'): link = 'http://weibo.cn/%s' % link

        #手动跳转到微博页面
        #result=self.fetch(link,"")
        #page1=page.decode('utf-8')
        #a=page1.find('如果没有自动跳转,请<a href="')
        #b=page1.find('">点击这里')
        #link=page1[a+19:b]
        #result=self.fetch(link, "")
        #link="http://weibo.cn/search/mblog?hideSearchFrame=&keyword=金融&advancedfilter=1&hasori=1&starttime=20141001&endtime=20141005&sort=hot&hasv=1&page=2"
        #result=self.fetch(link, "").decode('utf-8')

        #保存cookie
        if cookie_filename is not None:
            self.cj.save(filename=cookie_filename)
        elif self.cj.filename is not None:
            self.cj.save()
        print 'login success!',data
        #print link
        #print result
        #print page1
        

    def fetch(self, url,data):
        print 'fetch url: ', url
        req = urllib2.Request(url,data, headers=self.headers)
        return urllib2.urlopen(req).read()

#开始运行
#fet=Fetcher()
#fet.login("management1002@163.com","management1002")
