import itchat
from utils import scheduler
import events
print('欢迎使用HanayoriBot(WeChat版)！版本v0.1 By:鹿乃ちゃんの猫')
print('请使用手机端扫码登录')
itchat.auto_login(hotReload=True,enableCmdQR=2)
print('登录成功！')
scheduler.start()
itchat.run()
print('检测到手机端已登出，为了您的账号安全本程序自动登出！')
input('按任意键退出程序')