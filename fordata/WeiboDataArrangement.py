# coding=utf-8
'''
Created on 2014-10-15

@author: LuDan

根据SinaweiboData.py的处理结果，进一步解析数据内容，整理成需要的格式，并将微博内容单列出来形成微博内容文件
'''
import os
import re
import codecs

dir5=codecs.open(r"E:\Other\USTB\nlp\WeiboComment\WeiboCommentList.txt","w","utf-8")
for filename in os.listdir(r'E:\Other\USTB\nlp\WeiboData'):
    file1=codecs.open("E:\\Other\\USTB\\nlp\\WeiboData\\"+filename,"r","utf-8")
    dir=codecs.open(r"E:\Other\USTB\nlp\WeiboDataArrangemen\WeiboDataArrangemen_"+filename[10:],"w","utf-8")
    dir2=codecs.open(r"E:\Other\USTB\nlp\WeiboDataText\WeiboDataTextCV_"+filename[10:],"w","utf-8")
    dir3=codecs.open(r"E:\Other\USTB\nlp\WeiboDataText\WeiboDataTextPV_"+filename[10:],"w","utf-8")
    dir4=codecs.open(r"E:\Other\USTB\nlp\WeiboDataText\WeiboDataTextNV_"+filename[10:],"w","utf-8")
    dir.writelines('微博用户<b>用户首页<b>个人认证<b>机构认证<b>微博会员<b>微博ID<b>微博内容<b>获赞数<b>转发数<b>评论数<b>评论链接<b>发表时间<b>来源<b>链接\n'.decode("utf-8"))
    for line in file1.readlines():
        #line=line.decode('utf-8')
        UserSite=line.split('">')[0]
        line1=line.replace(UserSite+'">','')
        WeiboUser1=line1.split(':')[0]
        WeiboCV=''
        WeiboPV=''
        WeiboVIP=''
        if WeiboUser1.find(';;;hasCV')!=-1:
            WeiboCV='1'
            WeiboPV='0'
            WeiboUser1=WeiboUser1.replace(';;;hasCV','')
            if WeiboUser1.find(';;;hasVIP')!=-1:
                WeiboVIP='1'
                WeiboUser=WeiboUser1.replace(';;;hasVIP','')
            else:
                WeiboVIP='0'
                WeiboUser=WeiboUser1
        else:
            WeiboCV='0'
            if WeiboUser1.find(';;;hasPV')!=-1:
                WeiboPV='1'
                WeiboUser1=WeiboUser1.replace(';;;hasPV','')
                if WeiboUser1.find(';;;hasVIP')!=-1:
                    WeiboVIP='1'
                    WeiboUser=WeiboUser1.replace(';;;hasVIP','')
                else:
                    WeiboVIP='0'
                    WeiboUser=WeiboUser1
            
        a=line1.find(':')
        other=line1[a+1:]
        WeiboText=other.split('&nbsp;赞['.decode('utf-8'))[0]
        WeiboText=WeiboText.replace('&nbsp;原图'.decode('utf-8'),'')
        a=other.find('&nbsp;赞['.decode('utf-8'))
        other=other[a+8:]
        b=other.find(']')
        WeiboLike=other[:b]
        a=other.find('?uid=')
        WeiboID=other[a+5:a+15]
        a=other.find('">转发['.decode('utf-8'))
        other=other[a+5:]
        b=other.find(']')
        WeiboRepost=other[:b]
        other=other[b+1:]
        b=other.find('" class="cc"')
        WeiboComLink=other[:b]
        a=other.find('">评论['.decode('utf-8'))
        other=other[a+5:]
        b=other.find(']')
        WeiboComment=other[:b]
        a=other.find('收藏&nbsp;'.decode('utf-8'))
        other=other[a+8:]
        b=other.find('&nbsp;来自'.decode('utf-8'))
        WeiboTime=other[:b]
        WeiboSource=other[b+8:-1]
        if WeiboText.find('http://')>=0:
            a=WeiboText.find('http://')
            WeiboLink=WeiboText[a:a+19]
            re_a=re.compile('[^a-zA-Z0-9:/_.e]')
            a=re_a.sub('',WeiboLink)
            WeiboLink=a
            WeiboText2=WeiboText.replace(WeiboLink,'')
        else:
            WeiboLink='0'
            WeiboText2=WeiboText
        dir.writelines(WeiboUser+'<b>'+UserSite+'<b>'+WeiboPV+'<b>'+WeiboCV+'<b>'+WeiboVIP+'<b>'+WeiboID+'<b>'+WeiboText+'<b>'+WeiboLike+'<b>'+WeiboRepost+'<b>'+WeiboComment+'<b>'+WeiboComLink+'<b>'+WeiboTime+'<b>'+WeiboSource+'<b>'+WeiboLink+'\n')
        #re_h=re.compile(u"[^\u2e80-\u9fff]")
        #WeiboText2=re_h.sub('',WeiboText2)
        if WeiboCV is '1':
            dir2.writelines(WeiboText2+'\n')
        if WeiboPV is '1':
            dir3.writelines(WeiboText2+'\n')
        else:
            dir4.writelines(WeiboText2+'\n')
        if WeiboComment is not '0':
            dir5.writelines(WeiboID+','+WeiboComLink+'\n')
        
    dir.close()
    dir2.close()
    dir3.close()
    dir4.close()
    
dir5.close()
print 'ok'
    
    