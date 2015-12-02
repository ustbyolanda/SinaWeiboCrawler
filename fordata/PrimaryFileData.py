# coding=utf-8

import urllib2
import socket
import io
import gzip
import LoginWeibo3g2 as login
import time
import sys
import codecs
'''
Created on 2014-9-22

@author: LuDan

根据关键词、起止时间抓取初始网页
'''

fet=login.Fetcher()
fet.login("ustbtest01@sina.com","ludantest")
req_timeout=40
req_header={'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}

#keyword
keyword="股市"
#开始时间
starttime=20150928
#结束时间
endtime=20150928
#排序，实时time or 热门hot
sort="hot"

urls=[]
word=keyword.decode('utf-8').encode('gbk')
for time1 in range(starttime,endtime+1):
    directory=codecs.open(r"E:\Other\USTB\nlp\PrimaryFile\PrimaryFile_"+str(time1)+"_"+str(time1)+".txt","a","utf-8")
    #确定页数
    while True:
        try:
            req=urllib2.Request("http://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&advancedfilter=1&hasori=1&starttime="+str(time1)+"&endtime="+str(time1)+"&sort="+sort+"&page=1&vt=4",None,req_header)
            resp=urllib2.urlopen(req,None,req_timeout).read()
            result=resp.decode("utf-8")
            a=result.find('<body>')
            b=result.find('</html>')
            rres=result[a:b]
            directory.write(rres+'\n')
            #print rres
            break
        except Exception as e:
            print e
            print 'retry'
    a=rres.find('页</div></form></div><div class="pm" ><span class="pmf">'.decode('utf-8'))
    page=rres[a-3:a]
    if page.find('/')!=-1:
        st=page.find('/')+1
        page=page[st:]
    page=int(page)
    
    for i in range(2,page+1):
        urls.append("http://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&advancedfilter=1&hasori=1&starttime="+str(time1)+"&endtime="+str(time1)+"&sort="+sort+"&page="+str(i)+"&vt=4")
        
    while len(urls):
        for url in urls:
            try:
                req=urllib2.Request(url,None,req_header)
                resp=urllib2.urlopen(req,None,req_timeout).read()
                #resp=fet.fetch(url,"")
                #若网站将网页用gzip压缩，则使用下面三行进行解析
                #result1=resp.read()
                #bi=io.BytesIO(result1)
                #result=gzip.GzipFile(fileobj=bi,mode="rb").read().decode("utf-8")
                result=resp.decode("utf-8")
                a=result.find('<body>')
                b=result.find('</html>')
                rres=result[a:b]
                directory.write(rres+'\n')
                print url
                urls.remove(url)
            except Exception as e:
                print e
                print 'failed'
                pass
            time.sleep(5)
directory.close()
print 'ok'