#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import random
import smtplib
import sys
import time
import urllib.parse
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import cv2
import numpy as np
import requests
import urllib3
from lxml import etree

# import sys
urllib3.disable_warnings()

# print(sys.argv[0].strip("youthSpider.py"))
class FkYouthStudy:
    path = sys.argv[0].replace("/youthSpider.py", "")
    def run(self):
        self.openid = ""  # 只需填入自己的openid
        if self.openid == "":
            print("请填入openid")
            return
        self.get_jpg(self.get_str())
        self.submit_data(self.get_data())
        self.mail()

    def get_data(self):
        return requests.get("https://api.fjg360.cn/index.php", params={
            'm': 'vote',
            'c': 'index',
            'a': 'get_members',
            'openid': self.openid,
            "callback": "jQuery190{}_{}".format(str(random.random()).replace(".", ""), int(time.time() * 1000)),
            "_": int(time.time_ns())
        },verify=False)

    def submit_data(self, n):
        n = json.loads(n.text.split("(")[1].strip(")"))
        data = { # 这里建议自己抓包，接口是https://cp.fjg360.cn/index.php
            'm': 'vote',
            'c': 'index',
            'a': 'save_door',
            'username': n["h5_ask_member"]["name"],
            "openid": self.openid, # 你的openid
            'city': n["h5_ask_member"]["danwei1"], # 大学名字
            'danwei2': n["h5_ask_member"]["danwei2"], # xx班团支部
            'danwei': n["h5_ask_member"]["danwei3"], # xx学院
            'lesson_name': urllib.parse.quote(self.title),
            '_':int(time.time() * 1000),
            'sessionId':'',
            'imgTextId':'',
            'ip':'',
            'phone':'未知',
            'num':10,
            "callback": "jQuery190{}_{}".format(random.random(), int(time.time() * 1000))
        }
        headers = {
        "accept": "text / javascript,application / javascript, application / ecmascript, application / x - ecmascript, * / *; q = 0.01",
        "User-Agent": "ozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "x-requested-with": "XMLHttpRequest",
        "sec - fetch - site": "same - origin",
        "sec - fetch - mode": "cors",
        "sec - fetch - dest": "empty",
        "accept - encoding": "gzip, deflate, br",
        "accept - language": "zh - CN, zh;q = 0.9, en - US;q = 0.8, en;q = 0.7"
        }
        requests.get('https://cp.fjg360.cn/index.php', params=data, verify=False,headers=headers)

    def get_jpg(self, h):  # 切割图片
        if os.path.exists(self.path + "/tmp"):
            for i in os.listdir(self.path + "/tmp"):
                os.remove(self.path + "/tmp/" + i)
        else:
            os.mkdir(self.path + "/tmp")
        response = requests.get('https://h5.cyol.com/special/daxuexi/' + h + '/images/end.jpg', verify=False).content

        f = open("{}.jpg".format(self.path + "/tmp/tmp1"), mode="wb")
        f.write(response)
        f.close()
        image = cv2.imread(self.path + "/tmp/tmp1.jpg")
        imagetemp1 = cv2.imread(self.path + "/1.jpg")
        image1 = cv2.resize(image,(1170, 2008),interpolation=cv2.INTER_AREA)
        imagetemp = cv2.imread(self.path + "/temp.jpg")
        image2 = cv2.resize(imagetemp,(1170,275),interpolation=cv2.INTER_AREA)
        imagetemp1 = cv2.resize(imagetemp1,(1170,249),interpolation=cv2.INTER_AREA)
        image3 = np.vstack([image2,image1,imagetemp1])
        cv2.imencode('.jpg', image3)[1].tofile(self.path + r'/tmp/{}.jpg'.format(self.title))

    def get_str(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Host": "h5.cyol.com"
        }
        response = requests.get('http://h5.cyol.com/special/weixin/sign.json', headers=headers, verify=False)
        dict1 = json.loads(response.text)
        for i in dict.__reversed__(dict1):
            self.url = dict1[i]["url"]
            break
        url_str = dict1[i]["url"].split('/')
        response = requests.get(self.url,headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
        },verify=False)
        etree.HTMLParser(encoding="utf-8")
        # tree = etree.parse(local_file_path)
        tree = etree.HTML(response._content.decode("utf-8"))
        self.title = tree.xpath("/html/head/title")[0].text
        return url_str[5]

    def mail(self):
        ret = True
        try:
            my_sender = ''  # 发件人邮箱账号
            my_pass = ''  # 发件人邮箱密码
            my_user = ''  # 收件人邮箱账号，我这边发送给自己
            message = MIMEMultipart()
            m_img = MIMEBase('', '')
            m_img.add_header('Content-Disposition', 'attachment', filename="{}.jpg".format(self.title))
            fd = open("{}.jpg".format(self.path + "/tmp/"+self.title), "rb")  # 读取本地图片
            m_img.set_payload(fd.read())
            encoders.encode_base64(m_img)
            message.attach(m_img)
            message['From'] = Header(my_sender)  # 一定要是自己的邮件
            message['Subject'] = Header('{}'.format(self.title+ "  "))

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, my_user, message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            fd.close() # 打开以后一定要关闭
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
            print(e)
        return ret


if __name__ == "__main__":
    spider = FkYouthStudy()
    spider.run()
