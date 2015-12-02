# coding=utf-8
'''
Created on 2014-11-05

@author: LuDan

爬取新浪微博名人堂中财经分类下的名人微博
'''

import urllib2
import re
import LoginWeibo3g2 as login
import socket
import os
import string
import time

fet=login.Fetcher();
fet.login("management1002@163.com","management1002")
req_timeout=20
req_header={'User-Agent':'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9',
                   'Referer':''}
starttime='20131101'
endtime='20141101'

dir2=file(r'E:\graduate\public opinion analysis on financial risk\material\code\test\WeiboComment\UserWeiboComment.txt','w')
for filename in os.listdir(r'E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList'):
    urls=[]
    file1=open('E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserList\\'+filename,'r')
    for line in file1.readlines():
        link=line.split(',')[1]
        if link!='用户ID':
            urls.append('http://weibo.cn/'+link+'/profile?hasori=1&haspic=0&starttime='+starttime+'&endtime='+endtime+'&advancedfilter=1&page=1')
    print filename+':',urls
    while len(urls):
        for url in urls:
            page=1
            time.sleep(3)
            while True:
                try:
                    req=urllib2.Request(url,None,req_header)
                    resp=urllib2.urlopen(req,None,req_timeout).read()
                    result=resp.decode("utf-8")
                    result=resp.decode("utf-8")
                    break
                except:
                    print 'retry'
            a=result.find('下页'.decode('utf-8'))
            if a!=-1:
                a=result.find('页</div></form></div><div class="pm">')
                page1=result[a-4:a]
                b=page1.find('/')
                if b!=-1:
                    page=page1[b+1:]
            else:
                page=1
            page=int(page)
            urls1=[]
            for i in range(1,page+1):
                urls1.append(url[:-1]+str(i))
            print urls1
            dir=file('E:\\graduate\\public opinion analysis on financial risk\\material\\code\\test\\UserWeiboData\\'+url[16:26]+'.txt','w')
            while len(urls1):
                for url1 in urls1:
                    time.sleep(3)
                    try:
                        req=urllib2.Request(url1,None,req_header)
                        resp=urllib2.urlopen(req, None, req_timeout).read()
                        result=resp.decode("utf-8")
                        a=result.find('筛选'.decode('utf-8'))
                        b=result.find('<input type="submit" name="smblog" value="搜微博" />'.decode('utf-8'))
                        rres=result[a+2:b]
                        re_h=re.compile('(下页(.*))?(上页(.*))?页</div></form></div><div class="pm">'.decode('utf-8'))
                        rres1=re_h.sub('',rres)
                        rres1=rres1.replace('</span></div></div><div class="s"></div>','\n')
                        rres1=rres1.replace('<a href="http://weibo.cn/comment/','http://weibo.cn/comment/')
                        re_h1=re.compile('<[^>]+>')
                        rres2=re_h1.sub('',rres1)
                        rres2=rres2.replace('原图&nbsp;'.decode('utf-8'),'')
                        rres2=rres2.replace('&nbsp','')
                        rres2=rres2.replace('" class="cc">',';')
                        dir.write(rres2)
                        re_h5=re.compile('http://weibo.cn/comment/(.*)#cmtfrm')
                        #b=re_h5.search(rres2)
                        #print b.group()
                        #dir2.writelines(b.group())
                        print url1
                        
                        urls1.remove(url1)
                    except:
                        print 'retry:'+url1
                        pass
            dir.close()
            urls.remove(url)
                
                        
                
                
            
            
    
        