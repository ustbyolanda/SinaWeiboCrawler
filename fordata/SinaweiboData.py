# coding=utf-8
'''
Created on 2014-9-22

@author: LuDan

解析抓取的初始网页，只留下有用的信息
'''

import re
import os
import codecs

for filename in os.listdir(r"E:\Other\USTB\nlp\PrimaryFile"):
    filename=filename.decode('gbk').encode('utf-8')
    file1=codecs.open("E:\\Other\\USTB\\nlp\\PrimaryFile\\"+filename,'r',"utf-8")
    directory=codecs.open(r"E:\Other\USTB\nlp\WeiboData\WeiboData_"+filename[12:33],"w","utf-8")
    text=file1.read()
    text2=text.replace('</span></div></div><div class="s">','\n')
    text2=text2.replace('<img src="http://u1.sinaimg.cn/upload/2011/07/28/5338.gif" alt="V"/>',';;;hasPV')
    text2=text2.replace('<img src="http://u1.sinaimg.cn/upload/2011/07/28/5337.gif" alt="V"/>',';;;hasCV')
    text2=text2.replace('<img src="http://u1.sinaimg.cn/upload/h5/img/hyzs/donate_btn_s.png" alt="M"/>',';;;hasVIP')
    text2=text2.replace('<a class="nk" href="','')
    text2=text2.replace('http://weibo.cn/repost/','>')
    text2=text2.replace('</a>&nbsp;<a href="http://weibo.cn/comment/','http://weibo.cn/comment/')
    re_h1=re.compile("首页(.*)实时-热门".decode('utf-8'))
    re_h2=re.compile("(下页(.*))?(&nbsp;上页(.*))?(返回页面顶部(.*)语音weibo.cn(.*))?]\n".decode('utf-8'))
    re_h3=re.compile('<[^>]+>')
    text3=re_h3.sub('',text2)
    text4=re_h1.sub('',text3)
    text5=re_h2.sub('',text4)
    directory.write(text5)
    directory.close()
    
print 'ok'