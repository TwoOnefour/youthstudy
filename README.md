# Description
湖北地区的青年大学习自动打卡，本程序适合ios+qq自带的qq邮箱提醒直接开盖使用
# Usage
## Modify crontab configuration
整个文件夹下载到linux上，下载geckodriver到/usr/local/bin文件夹下，使用crontab，配置如下

<code>57 23 * * * rm -rf /home/admin/myYouthStudy/tmp/*</code>

<code>0 12 * * 1 python3 /home/admin/myYouthStudy/youthSpider.py > /root/youthSpider.log 2>&1 </code>

:wq保存

注意，crontab中的/home/admin的路径请改为你自己的路径，youthSpider.log必须赋予权限

<code>chmod +x /root/youthSpider.log</code>

## Modify the necessary information

### Smtp information
使用qq邮箱，授权码请自己去qq邮箱获取，位于141行

![image](https://user-images.githubusercontent.com/77989499/224948420-db673881-f68c-4b59-b1d2-d16eb9662cea.png)

如果想使用别的邮箱，请修改smtp服务器，位于154行

![image](https://user-images.githubusercontent.com/77989499/224948956-11a88f02-233c-436e-9345-9eca59499a4f.png)
### Submit information

![image](https://user-images.githubusercontent.com/77989499/224949294-521fcece-04bb-4197-a814-fe2596a3b4c6.png)

建议自行抓包填写

### Not a user of IOS?
如果不是ios用户，可以自行修改截图图片部分

![image](https://user-images.githubusercontent.com/77989499/224949571-c9d41b4e-ae46-45d5-881a-c9ba09eefe88.png)

# (NOTE)IT MAY NOT WORK

由于没有鉴别手段，无法验证接口正确性，建议只当作一个自动截图使用，不保证后台是否有观看数据。
![558E4669DE897CF0A70183480A5FFC8A](https://user-images.githubusercontent.com/77989499/224951932-412fd8f3-b170-48e7-a46e-51b86cd4b449.png)

![UEPQ5E3`7ASFN X`P1A3F6F](https://user-images.githubusercontent.com/77989499/224951217-7bbb7458-9fd3-48d9-92d6-a478c2b6332e.png)

![)T~T0Q1(1TORCK9(LF4%W$4](https://user-images.githubusercontent.com/77989499/224951245-e3b4ab60-8053-4ab0-ac1c-f2d870d9bbb7.png)

