## RenewRemind - 一个 小说/番剧/漫画/知乎文章 更新提醒脚本

## 简介
关注的 **小说/番剧/漫画/知乎文章** 如果有更新，立刻给你发送提醒邮件。

脚本中内置了一部漫画和两部小说的更新检查。

第一次运行会发送它们的当前更新情况到你的邮箱。

你可以自行修改代码中的更新检查对象。

如果你有linux云服务器，可以用crontab设置隔一段时间就运行脚本，这样就可以24小时时时刻刻监控更新情况啦！

该脚本仅供参考。
## 如何使用
### step 1. 将项目clone到本地

```
git clone https://github.com/roachsinai/RenewRemind.git
```

### step 2. 设置email用户名和授权码

![设置email用户名和授权码](https://github.com/windcode/renewremind/raw/master/screenshots/1.png)

授权码获取方式：[什么是授权码，它又是如何设置？ - qq邮箱帮助中心](http://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28)

### step 3. 运行脚本

```
python renewremind/renewremind.py
```

`crontab`设置：

```
$ crontab -e # 新建或者编辑已有的cron table

选择`vim`进行编辑输入：
*/10 * * * * /root/remind/renewRemind.py # 10min检查一次
```

运行脚本会检查更新情况，如果有更新，发送提醒邮件给你。

初次运行会发送当前更新情况。

## 运行截图

初次运行

![初次运行](https://github.com/windcode/renewremind/raw/master/screenshots/2.png)

收到提醒邮件

![收到邮件](https://github.com/windcode/renewremind/raw/master/screenshots/3.png)

重写函数可以定制更新检查对象

![更新检查函数](https://github.com/windcode/renewremind/raw/master/screenshots/4.png)


## 注意

* 脚本默认仅支持qq邮箱。若要支持其它邮箱，请自行修改代码。
* 测试环境为linux




