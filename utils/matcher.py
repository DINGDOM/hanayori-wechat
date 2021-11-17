from . import patterner
import re
import itchat
import threading
from itchat.content import *
def pattern_command(msg):
    for key,value in patterner.COMMAND.items():
        state=re.match(key,msg.text)
        if state!=None:
            matcher=threading.Thread(target=value,args=(msg,msg.text[state.span()[1]:].strip()))
            matcher.start()
            break
@itchat.msg_register(TEXT)
def text_reply(msg):
    chat=itchat.search_friends(userName=msg.fromUserName)
    print('收到来自好友: %s 的消息: %s'%(chat['NickName'],msg.text))
    pattern_command(msg)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.text=msg.text.split(u'\u2005')[1]
        chat=itchat.search_chatrooms(userName=msg.fromUserName)
        print('收到来自群聊: %s 的 %s 的消息: %s'%(chat['NickName'],msg.actualNickName,msg.text))
        pattern_command(msg)