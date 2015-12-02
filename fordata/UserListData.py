# coding=utf-8
'''
Created on 2014-11-05

@author: LuDan

爬取新浪微博名人堂中财经分类下的名人信息
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

fet=login.Fetcher();
fet.login("management1002@163.com","management1002")
req_timeout=20
req_header={'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}

typelist=['经济学,54','能源,1720','其他,505','理财,59','财经行业高管,1862','人力资源管理,2120','财经行业公司,2130','会计,952','保险,663','外汇,57','基金,56','股票,55','期货,58','投资,518','商界名人,53','管理,516','银行,664']
for types in typelist:
    type=types.split(',')[0]
    num=types.split(',')[1]
    urls=[]
    urlp='http://weibo.cn/v2star/?tagname=财经&subcatname='+type+'&cat=1&subcat='+num+'&lcat=1&sorttype=industry&page=1'
    #确定页数
    while True:
        try:
            req=urllib2.Request(urlp,None,req_header)
            resp=urllib2.urlopen(req,None,req_timeout).read()
            result=resp.decode("utf-8")
            print 'ok'
            break
        except:
            print 'retry'
    a=result.find('下页'.decode('utf-8'))
    page=20
    if a!=-1:
        a=result.find('页</div></form></div><div class="cd"><a'.decode('utf-8'))
        page=result[a-2:a]
        if page.find('/')!=-1:
            page=page[1:]
            
    else:
        page=1
        
    page=int(page)    
    dir=file("E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList\\UserList"+type.decode('utf-8').encode('gbk')+".txts",'w')
    for i in range(1,page+1):
        url='http://weibo.cn/v2star/?tagname=财经&subcatname='+type+'&cat=1&subcat='+num+'&lcat=1&sorttype=industry&page='+str(i)
        urls.append(url)
        
    while len(urls):
        for url in urls:
            try:
                req=urllib2.Request(url,None,req_header)
                resp=urllib2.urlopen(req, None, req_timeout).read()
                result=resp.decode("utf-8")
                a=result.find('更新'.decode('utf-8'))
                b=result.find('关注以上这些人'.decode('utf-8'))
                rres=result[a+12:b]
                re_h=re.compile('<div class="c"><form action="http:(.*)<input type="submit" value="')
                rres1=re_h.sub('',rres)
                rres1=rres1.replace('</div>','\n')
                rres1=rres1.replace('</a></td><td valign="top"><a href="/u/','')
                dir.write(rres1)
                print url
                urls.remove(url)
            except:
                print 'failed: '+url
                pass
            time.sleep(5)
    dir.close()
    
for filename in os.listdir(r'E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList'):
    #filename=filename.decode('gbk').encode('utf-8')
    file1=open('E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList\\'+filename,'r')
    dir2=file('E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList\\'+filename[:-1],'w')
    dir2.write('用户名,用户ID,粉丝数\n')
    for line in file1.readlines():
        line=line.decode('utf-8')
        a=line.find('class="por" />')
        userid=line[a+14:a+24]
        line=line[a+24:]
        b=line.find('</a>')
        username=line[2:b]
        line=line[b+4:]
        c=line.find('粉丝'.decode('utf-8'))
        d=line.find('人'.decode('utf-8'))
        fans=line[c+2:d]
        dir2.write(username+','+userid+','+fans+'\n')
    dir2.close()
    file1.close()
    os.remove('E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList\\'+filename)
        
    