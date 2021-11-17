import itchat
def isGroup(msg):
    if '@@'in msg.fromUserName :
        return True
    else:
        return False
def GetGroupName(msg):
    chat=itchat.search_chatrooms(userName=msg.fromUserName)
    if chat!=[]:
        return chat['NickName']
    else:
        return ''
def GetFriendName(msg):
    chat=itchat.search_friends(userName=msg.fromUserName)
    if chat!=[]:
        return chat['NickName']
    else:
        return ''
def GetGroupID(name):
    chat=itchat.search_chatrooms(name=name)
    if chat!=[]:
        return chat[0]['UserName']
    else:
        return ''
def GetFriendID(name):
    chat=itchat.search_friends(name=name)
    if chat!=[]:
        return chat[0]['UserName']
    else:
        return ''
def At(name='all'):
    if name=='all':
        return '@所有人\u2005'
    else:
        return '@%s\u2005'%(name)