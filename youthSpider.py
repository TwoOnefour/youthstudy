#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cv2
import numpy as np
from pyvirtualdisplay import Display
import time
import sys
import urllib.parse
import execjs
import requests
import json
from lxml import etree
import cn2an
import os
import smtplib
import urllib3
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
urllib3.disable_warnings()
class fkYouthStudy():
    def run(self):
        name = '' # 你自己的名字


        self.get_jpg()

        self.mail()

    def submit_data(self,name, n):
        data = { # 这里建议自己抓包，接口是https://cp.fjg360.cn/index.php
            'm': 'vote',
            'c': 'index',
            'a': 'save_door',
            'username': name,
            "openid": "", # 你的openid
            'city': '', # 大学名字
            'danwei2': '', # xx班团支部
            'danwei': '', # xx学院
            'lesson_name': '"青年大学习"2023年第' + n + '期',
            '_':int(time.time() * 1000),
            'sessionId':'',
            'imgTextId':'',
            'ip':'',
            'phone':'未知',
            'num':10,
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
        response = requests.get('https://cp.fjg360.cn/index.php', params=data, verify=False,headers=headers)



    def get_jpg(self): # 切割图片
        h = self.get_str()
        self.jstopy()
        response = requests.get('https://h5.cyol.com/special/daxuexi/' + h + '/images/end.jpg', verify=False).content
        f = open("{}.jpg".format("/home/admin/myYouthStudy/tmp/tmp1"), mode="wb")
        f.write(response)
        f.close()
        image = cv2.imread("/home/admin/myYouthStudy/tmp/tmp1.jpg")
        imagetemp1 =  cv2.imread("/home/admin/myYouthStudy/1.jpg")
        image1 = cv2.resize(image,(1170, 2008),interpolation=cv2.INTER_AREA)
        imagetemp = cv2.imread("/home/admin/myYouthStudy/temp.jpg")
        image2 = cv2.resize(imagetemp,(1170,275),interpolation=cv2.INTER_AREA)
        imagetemp1 = cv2.resize(imagetemp1,(1170,249),interpolation=cv2.INTER_AREA)
        image3 = np.vstack([image2,image1,imagetemp1])

        cv2.imwrite("/home/admin/myYouthStudy/tmp/{}.jpg".format(self.title), image3)
    

    def get_str(self):
        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        #     'Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        #     "Accept-Encoding": "gzip, deflate",
        #     'Host':'news.cyol.com'
        # }
        #
        # response = requests.get('http://news.cyol.com/gb/channels/vrGlAKDl/index.html', headers=headers, verify=False)
        # f = open("mainhtml.html", mode="wb")
        # f.write(response.content)
        # # local_file_path = './大.html'
        # parser = etree.HTMLParser(encoding="utf-8")
        # # tree = etree.parse(local_file_path)
        # tree = etree.HTML(response.text)
        # # result = tree.xpath('//ul[@class="movie-list"]/text()')
        # try:
        #     result = dict(tree.xpath("/html/body/div[2]/div/ul/li[1]/h3/a")[0].attrib)["href"]
        #     self.url = result
        # except IndexError as e:
        #     print("爬虫限制")
        #     self.close()
        # url_str = result.split('/')
        # f.close()
        # return url_str[5]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Host": "h5.cyol.com"
        }
        response = requests.get('http://h5.cyol.com/special/weixin/sign.json', headers=headers, verify=False)
        dict1 = json.loads(response.text)
        count = 0
        for i in dict1:
            if count == len(dict1) - 1:
                self.url = dict1[i]["url"]
            count += 1
        url_str = dict1[i]["url"].split('/')
        response = requests.get(self.url,headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
        },verify=False)
        response = requests.get(self.url,headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
        },verify=False)
        parser = etree.HTMLParser(encoding="utf-8")
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
            m_img.add_header('Content-Disposition', 'attachment', filename="{}   .jpg".format(self.title))
            fd = open("{}.jpg".format("/home/admin/myYouthStudy/tmp/"+self.title), "rb")  # 读取本地图片
            m_img.set_payload(fd.read())
            encoders.encode_base64(m_img)
            message.attach(m_img)
            message['From'] = Header('1')
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
    def close(self):
        sys.exit()
    def jstopy(self):
        display = Display(visible=0, size=(900, 800))
        display.start()  # 显示界面的设置
        browser = webdriver.Firefox(executable_path="{}/geckodriver".format("/usr/local/bin"))
        lesson_name = urllib.parse.quote(self.title)
        # https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&username=%E8%93%9D%E6%A5%A0%E6%A5%A0&openid=omLPUjiM4XOmfhlBKLawP2p9fWZ0&city=%E6%AD%A6%E6%B1%89%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&danwei2=%E7%89%A9%E7%AE%A12001%E5%9B%A2%E6%94%AF%E9%83%A8&danwei=%E4%BA%A4%E9%80%9A%E4%B8%8E%E7%89%A9%E6%B5%81%E5%B7%A5%E7%A8%8B%E5%AD%A6%E9%99%A2&lesson_name="青年大学习"2022年第28期&_=${Date.now()}&sessionId=&imgTextId=&ip=&phone=%E6%9C%AA%E7%9F%A5&num=10
        with open("{}/index.html".format("/home/admin/myYouthStudy/tmp"),"w") as f:
            f.write('''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>mytestpage</title>

<style type = "text/css">

</style>
<script type="text/javascript" src="https://res.wx.qq.com/open/js/jweixin-1.0.0.js"></script>
<script type="text/javascript" src="https://lib.baomitu.com/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="http://cdnsite.fjg360.cn/jquery-1.9.1.min.js"></script>
<script charset="">
    function ajaxJsonp(){
	$.ajax({
				type: 'GET',
				url: `https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&username=%E8%93%9D%E6%A5%A0%E6%A5%A0&openid=omLPUjiM4XOmfhlBKLawP2p9fWZ0&city=%E6%AD%A6%E6%B1%89%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6&danwei2=%E7%89%A9%E7%AE%A12001%E5%9B%A2%E6%94%AF%E9%83%A8&danwei=%E4%BA%A4%E9%80%9A%E4%B8%8E%E7%89%A9%E6%B5%81%E5%B7%A5%E7%A8%8B%E5%AD%A6%E9%99%A2&lesson_name='''+lesson_name+'''&_=${Date.now()}&sessionId=&imgTextId=&ip=&phone=%E6%9C%AA%E7%9F%A5&num=10`,
	        	dataType: 'jsonp',  //类型
	        	data:  null ,
				jsonp: 'callback', //jsonp回调参数，必需
				async: false,
				// error: errorHandle,
	        	// success: sucessHandle
	});
}
</script>
</head>
<body>

<button onclick="ajaxJsonp()">123123</button>
  <iframe frameborder="0" scrolling="no" style="width: 100%;height:1080px;"></iframe>
        <center style="padding: 0;margin:0;list-style: none">
            <br><a href="https://beian.miit.gov.cn">桂ICP备2022003330号</a>
        </center>

</body>
</html>''')
        # display = Display(visible=0, size=(900, 800))
        # display.start()  # 显示界面的设置

        wait = WebDriverWait(webdriver,10,0.5)
        browser.get("file://{}/index.html".format("/home/admin/myYouthStudy/tmp"))
        wait.until(lambda diver:browser.find_element(By.XPATH,"/html/body/button"))
        browser.find_element(By.XPATH,"/html/body/button").click()
        browser.close()
        display.stop()
if __name__ == "__main__":
    spider = fkYouthStudy()
    spider.run()
    # spider.jstopy()
