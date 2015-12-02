# coding=utf-8
'''
Created on 2014-10-20

@author: LuDan

爬取新浪微博中链接到的其他网站的长文本
'''

import urllib2
import sys
import re
import LoginWeibo3g2 as login
import socket
import chardet
import os
import string
import time
import httplib

fet=login.Fetcher();
fet.login("ustbtest01@sina.com","ludantest")
req_timeout=20
req_header={'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}


for filename in os.listdir(r'E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\WeiboDataArrangemen'):
    urls=[]
    file1=open("E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\WeiboDataArrangemen\\"+filename,"r")
    for line in file1.readlines():
        Link=line.split("<b>")[13]
        Link=Link.replace('\n','')
        if Link!="0" and Link!="链接":
            urls.append(Link)
    print filename+" : ",urls
    while len(urls):
        for url in urls:
            time.sleep(3)
            print url
            try:
                req=urllib2.Request(url,None,req_header)
                resp=urllib2.urlopen(req,None,req_timeout)
                #若网站将网页用gzip压缩，则使用下面三行进行解析
                #result1=resp.read()
                #bi=io.BytesIO(result1)
                #result=gzip.GzipFile(fileobj=bi,mode="rb").read().decode("utf-8")
                result1=resp.read()
                infoencode=chardet.detect(result1).get('encoding','utf-8')
                if infoencode is not None:
                    result=result1.decode(infoencode,'ignore')
                    a=result.find('<body>')
                    b=result.find('</html>')
                    if a!=-1 and b!=-1:
                        result=result[a:b]
                    sstr=url[-7:]
                    delset = string.punctuation
                    sstr1=sstr.translate(None,delset)
                    re_a=re.compile('\W')
                    sstr2=re_a.sub('',sstr1)
                    dir=file("E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\WeiboLongText\\WeiboLongText_"+sstr2+".txt","w")
                    re_h=re.compile(u"[^\u2e80-\u9fff]")
                    text=re_h.sub('',result)
                    dir.write(text)
                    urls.remove(url)
                    dir.close()
                    print "succeed "+str(len(urls))
                else:
                    print "failed1"+"    removed"
                    urls.remove(url)
                    pass
                
            except socket.timeout:
                print "failed2:socket.timeout"
                pass
            except socket.error:
                print "failed3:socket.error"+"    removed"
                urls.remove(url)
                pass
            except urllib2.HTTPError:
                print "failed4:urllib2.HTTPError"+"    removed"
                urls.remove(url)
                pass
            except urllib2.URLError:
                print "failed5:urllib2.URLError"+"    removed"
                urls.remove(url)
                pass
            except httplib.BadStatusLine:
                print "failed5:httplib.BadStatusLine"+"    removed"
            

print 'ok'


