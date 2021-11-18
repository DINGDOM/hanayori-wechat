<!-- markdownlint-disable MD033 MD041-->
<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/kanomahoro/images@main/logo.png" width="200" height="200"/>
</p>

<div align="center">

# HanayoriBot(WeChat)
<!-- markdownlint-disable-next-line MD036 -->
_✨ 基于itchat-uos的B站动态推送与开播提醒机器人 ✨_

</div>

## 简介

本插件基于[itchat-uos](https://github.com/why2lyj/ItChat-UOS),由[HanayoriBot](https://github.com/kanomahoro/nonebot-hanayori)项目魔改而来,可以及时推送B站UP主动态至群聊；并且能够对B站主播的直播间状态进行实时监控，从而实现了主播开播提醒；有效避免了突击直播，无人问津的尴尬局面

名字由来：花寄女子寮(Hanayori Joshiryou) 花寄天下第一！！！！！（来自某花寄~~DD~~单推人）
+ 鹿乃ちゃん：B站(316381099)
+ 小东人魚Official：B站(441382432)
+ 花丸晴琉Official：B站(441381282)
+ 野野宫のののOfficial：B站(441403698)


## 即刻开始
python版本要求：<=3.9 >=3.7
### 如何使用
   1. pip install -r requirements.txt
   2. python main.py
### 指令说明
**在群聊中使用格式**：@机器人 指令 UID(如果指令要求的话) 
**在私聊中使用格式**：指令 UID(如果指令要求的话)
**所有指令如下：**
1. **关注 UID**
   添加新主播，UID为主播的B站UID
2. **取关 UID**
   取关主播，UID为主播的B站UID
3. **列表**
   显示当前关注列表
4. **开启动态 UID**
   开启B站动态推送
5. **关闭动态 UID**
   关闭B站动态推送
6. **开启直播 UID**
   开启开播提醒
7. **关闭直播 UID**
   关闭开播提醒
8. **开启全体 UID**
   开启开播@全体成员
9. **关闭全体 UID**
   关闭开播@全体成员
10. **帮助**
   顾名思义

### 遇到问题？
你可以直接提交issue，或者发送邮件到：kano@hanayori.top
### FAQ
1. Q：手机如果登出，本程序也会登出？
 - A：这是由于微信网页版本身的协议问题导致的，并非是Bug。你可以使用多开助手，手机登录多个微信号，然后杀掉机器人账号的应用后台，这不会使机器人登出。
2. Q：为什么群聊更名后推送列表为空？
 - A：同样是由于微信网页版协议的局限性所导致，目前没有解决办法。
3. Q: 第二次启动无法登录？
 - A：删除itchat.pkl文件后再重新启动，或者直接将main.py中的hotReload=True改为hotReload=False
4. Q：二维码在终端显示不全？
 - A：将main.py中的enableCmdQR=2改为enableCmdQR=True
   
### 效果展示

![效果1](https://cdn.jsdelivr.net/gh/kanomahoro/images@main/20211118.jpg)

![效果2](https://cdn.jsdelivr.net/gh/kanomahoro/images@main/20211118_1.jpg)
