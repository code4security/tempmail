#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import os
import time
from prettytable import PrettyTable
import json
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
import urllib3
urllib3.disable_warnings()

# proxies = {
#     'http': 'socks5://127.0.0.1:1080',
#     'https': 'socks5://127.0.0.1:1080'
# }
proxies = None
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': 'http://www.moakt.com/zh',
    'Origin': 'http://www.moakt.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b',
}
add_google_ad = {'__utmz': '213295240.1560941736.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                 '__utma': '213295240.364101931.1560941736.1560941736.1560994110.2',
                 '__utmb': '213295240.6.10.1560994110',
                 '__utmc': '213295240'
                 }

class AutoGetSsrLink():

    def __init__(self):
        self.mail = ''
        self.mail_count = 0
        self.mail_dict = {}
        self.s = requests.session()
        self.s.headers.update(headers)
        self.mail_table =PrettyTable(["序号", "链接", "标题"])
        requests.utils.add_dict_to_cookiejar(self.s.cookies, add_google_ad)

    # ①申请邮箱
    def init_mail(self):

        print '①开始申请邮箱...'
        self.s.get('https://www.moakt.com/zh', proxies=proxies)

        i = 0
        while i < 9:
            self.s.post('https://www.moakt.com/zh/mail',
                        data='mailhost=disbox.net&setemailaddress=&random=%E8%8E%B7%E5%BE%97%E4%B8%80%E4%B8%AA%E9%9A%8F%E6%9C%BA%E9%82%AE%E7%AE%B1%E5%9C%B0%E5%9D%80',
                        proxies=proxies)
            res = self.s.get('https://www.moakt.com/zh/mail', proxies=proxies)
            result = re.search(r'<div id="email-address">(\w+\@\w+\.\w+)</div>', res.text)

            if not result:
                print '获取邮箱失败，正在重新获取...尝试次数%s' % i
                i = i+1
            else:
                self.mail = result.group(1)
                break
        print '申请邮箱结束！'
        print '申请的邮箱地址为：[%s]' % self.mail

    # ②收信
    def get_mail_post(self):

        print '②开始收信...'
        while True:
            os.system("clear")
            print ('当前时间：%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            print '邮件地址：%s' % self.mail

            res = self.s.get('https://www.moakt.com/zh/mail', proxies=proxies).text
            # 邮件数量
            ccount = re.search(r'<strong>(\d+)</strong>', res)
            if ccount:
                print '邮件数量：%s' % ccount.group(1)
                id = int(ccount.group(1))
            else:
                ccount = 0
                id = ccount
                print '邮件数量：0'

            mail_list = re.findall(r'<td>.*<a.href="/zh/msg/[A-Z0-9\-]*?">.*?</a></td>', res)
            # 邮件编号

            if len(mail_list) > 0:
                for i in mail_list:
                    prefix = 'https://www.moakt.com'
                    msg_list = re.findall(r'href="(/zh/msg/[A-Z0-9\-]*?)">(.*?)</a>', i)
                    for j in msg_list:
                        # print id,j[0],j[1]
                        msg_url = prefix + j[0]
                        self.mail_table.add_row([id, msg_url, j[1]])
                        self.mail_dict.update({str(id): msg_url})
                        id = id - 1

            print self.mail_table
            id = len(self.mail_dict)

            if id != self.mail_count:
                self.mail_count = id
                input = raw_input("收到新邮件，是否马上阅读？[Y/N]")
                if input == 'Y':
                    uid = raw_input("请输入邮件序号:")
                    self.get_msg_post(uid)
                else:
                    self.mail_count = id
                    pass
            self.mail_table.clear()
            self.mail_table = PrettyTable(["序号", "链接", "标题"])
            time.sleep(5)

    def get_msg_post(self, uid):
        print uid
        print self.mail_dict[uid]
        print '读取内容中...'
        x = str(uid)
        url = self.mail_dict[x] + '/content'
        source = self.s.get(url, proxies=proxies).text
        os.system("clear")
        print source



if __name__ == '__main__':

    Auto = AutoGetSsrLink()
    # ① 初始化邮箱
    Auto.init_mail()

    # ② 收信
    Auto.get_mail_post()
  
