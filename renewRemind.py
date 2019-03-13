#!/usr/bin/python
#coding=utf8

import pickle
import re
import os,sys
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# import gi
# gi.require_version('Notify', '0.7')
# from gi.repository import Notify

timeout = 30                             # 超时时间
charset = 'utf-8'		# 请求页面的编码格式
subject = '【更新提示】'	# email 中的主题
content = ''			# email 中的内容
record_file = os.path.join(sys.path[0],'record.dat')      # 记录文件
conf_file = os.path.join(sys.path[0],'conf.ini')                # 配置文件
renew_dict = {}                 # 更新记录
my_email = ''                      # 邮箱地址
my_password = ''                   # 邮箱授权码

def get_html(url,timeout=None):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) KHTML/5.55.0 (like Gecko) Konqueror/5 KIO/5.55'}
    request = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(request,timeout=timeout)
    return response.read()

def send_email(sub,cont):
    # send email
    global my_email,my_password
    sender = my_email                   # 发送方
    receiver = [my_email]               # 收件方
    subject = sub                       # 邮件主题
    smtpserver = 'smtp.qq.com'          # 邮箱服务器
    username = my_email                 # 用户名
    password = my_password		# 授权码

    msg = MIMEText(cont, 'html', 'utf8')	# 设置内容
    msg['Subject'] = Header(subject, 'utf8')	# 设置主题
    msg['From'] = sender			# 设置发送方
    msg['To'] = ','.join(receiver)		# 设置接收方
    smtp = smtplib.SMTP_SSL(smtpserver,465)
    #smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def Init():
    global renew_dict,my_email,my_password
    print('正在加载邮箱地址和授权码……')
    try:
        fp = open(conf_file,'r')
    except Exception as e:
        print('加载失败，conf.ini文件不存在')
        raise Exception(e)
    lines = fp.readlines()
    my_email = lines[1].strip()     # 加载邮箱地址
    my_password = lines[3].strip()  # 加载邮箱授权码
    fp.close()

    print('正在加载更新记录……')
    # 提取更新情况记录
    try:
        fp = open(record_file,'rb')
    except:
        fp.close()
        return

    renew_dict = pickle.load(fp)
    fp.close()


def RenewCheck(key,src_url,des_url,pattern_str,charset):
    # 提示信息
    print('正在检查【%s】的更新状态……'%(key))

    # 检查更新
    global subject,content,isRenew,renew_dict
    isRenew = False
    # host = 'http://'+src_url.split('//')[1].split('/')[0]   # 检查网站的host地址
    html = get_html(src_url,timeout).decode(charset)        # 获得页面源码

    # 解析源码
    pattern = re.compile(pattern_str,re.S)
    items = re.findall(pattern,html)
    if items:
        items = items[0]
    else:
        return

    # 清洗数据
    title = items.strip()

    # 判断是否有更新
    cur = title.encode('utf8')
    if key in renew_dict: # 判断之前有无记录
        last = renew_dict[key]
    else:
        last = None

    if cur != last or last==None:
        # 如果有更新，发送邮件提示
        isRenew = True

        # 更新记录
        renew_dict[key] = cur
        fp = open(record_file,'wb')
        pickle.dump(renew_dict, fp)
        fp.close()

        print('【%s】有更新，发送邮件……'%(key))
        subject += '%s '%(key)
        content += '【%s】已经更新到【%s】，戳这里看详情：%s<br/>'%(key,cur.decode(),des_url)
    else:
        # 没有更新
        print('【%s】没有更新'%(key))


def main():
    global subject,content,isRenew

    # 提取更新情况记录
    Init()

    # 检查所有更新，并输出提示信息
    # 函数原型：
    # def RenewCheck( key,src_url,des_url,pattern_str,charset )
    # 参数介绍 :
    # key           - 检查对象，例如：西部世界、扳手少年等
    # src_url       - 检查对象的网站地址
    # des_url       - 如果有更新，提示中所指向的跳转地址
    # pattern_str   - 匹配正则表达式
    # charset       - 检查对象网站的编码
    renewObjList = [
        # ('扳手少年',\
        #     'http://ac.qq.com/Comic/ComicInfo/id/520794',\
        #     'http://ac.qq.com/ComicView/index/id/520794/cid/176',\
        #     r'<a class="works-ft-new" href=".*?">(.*?)</a><span.*?>.*?</span>',\
        #     'utf8'
        # ),  # 漫画：扳手少年
        # ('剑来',\
        #     'http://book.zongheng.com/book/672340.html',\
        #     'http://www.booktxt.net/5_5871/',\
        #     r'<div class="tit"><a href=".*?">(.*?)</a><em></em></div>',\
        #     'utf8'\
        # ),   # 小说：剑来
        # ('天行',\
        #     'http://www.17k.com/book/2722533.html',\
        #     'https://www.piaotian.com/html/9/9227/',\
        #     r'最新vip章节：<a\s*href=".*?"\s*target="_blank">(.*?)</a>',\
        #     'utf8'\
        # )   # 小说：天行
        ('渤海小吏',\
            'https://www.zhihu.com/people/dai-zong-66/posts',\
            'https://www.zhihu.com/people/dai-zong-66/posts',\
            r'<h2 class="ContentItem-title"><a href=".*?" target="_blank" rel="noopener noreferrer" data-za-detail-view-element_name="Title">(.*?)</a></h2>',\
            'utf8'\
        )   # 知乎：2300年封建脉络的百场转折之战
    ]

    for renewObj in renewObjList:
        try:
            RenewCheck(*renewObj)
        except Exception as e:
            print('[ERROR]:%s'%e)
            continue

    if isRenew:
        send_email(subject+'有更新！',content)
        # Notify.init ("Chasing")
        # result = Notify.Notification.new (subject+'有更新！',
        #                        content,
        #                        "dialog-information")
        # result.show()

if __name__ == '__main__':
    main()
    '''
    try:
        main()
    except Exception,e:
        print '[ERROR]:%s'%e

    '''
