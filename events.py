from utils import *
import data_source
import model
import itchat
model.Init()
live_index=0
dynamic_index=0

@scheduler.scheduled_job('cron',second='*/15',id='bilibili_live')
def live():#定时推送直播间状态
    if model.Empty():
        return
    global live_index
    anchors=model.GetAnchorList()
    live_index %=len(anchors)
    for index in range(live_index,len(anchors)):
        if anchors[index][3]==1:
            break
        live_index+=1
    if live_index==len(anchors):
        return
    status,live_status,content,media=data_source.LiveRoomInfo(anchors[live_index][0])
    if status!=0 or anchors[live_index][4]==live_status:
        live_index+=1
        return
    print('检测到 {} 直播状态更新'.format(anchors[live_index][1]))
    model.UpdateLive(anchors[live_index][0],live_status)
    cards=model.GetALLCard(anchors[live_index][0])
    media=data_source.download_media(media)
    for card in cards:
        if card[3]==1:#允许推送直播
            if card[1]==1:#是群聊
                if card[4]==1:#需要@全体成员
                    toUserName=GetGroupID(card[0])
                    itchat.send_msg(At()+content,toUserName)
                    for index in media:
                        itchat.send_image(index,toUserName)
                else:#不需要@全体成员
                    toUserName=GetGroupID(card[0])
                    itchat.send_msg(content,toUserName)
                    for index in media:
                        itchat.send_image(index,toUserName)
            else:#私聊
                toUserName=GetFriendID(card[0])
                itchat.send_msg(content,toUserName)
                for index in media:
                    itchat.send_image(index,toUserName)
    live_index+=1
    data_source.clean_media(media)
@scheduler.scheduled_job('cron',second='*/15',id='bilibili_dynamic')
def dynamic():#定时推送最新用户动态
    if model.Empty():
        return
    global dynamic_index
    anchors=model.GetAnchorList()
    dynamic_index %=len(anchors)
    status,dynamic_id,content,media= data_source.LatestDynamicInfo(anchors[dynamic_index][0])
    if status!=0 or anchors[dynamic_index][2]==dynamic_id:
        dynamic_index+=1
        return
    print('检测到 {} 动态更新'.format(anchors[dynamic_index][1]))
    model.UpdateDynamic(anchors[dynamic_index][0],dynamic_id)
    cards=model.GetALLCard(anchors[dynamic_index][0])
    media=data_source.download_media(media)
    for card in cards:
        if card[2]==1:#允许推送动态
            if card[1]==1:#是群聊
                toUserName=GetGroupID(card[0])
                itchat.send_msg(content,toUserName)
                for index in media:
                    itchat.send_image(index,toUserName)
            else:#私聊
                toUserName=GetFriendID(card[0])
                itchat.send_msg(content,toUserName)
                for index in media:
                    itchat.send_image(index,toUserName)
    dynamic_index+=1
    data_source.clean_media(media)
adduser = on_command('关注')
@adduser.msg#添加主播
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：关注 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)!=0:
                status=model.AddCard(args,id,is_group,anchor[3])
                if status==0:
                    msg='{}({})添加成功！'.format(anchor[1],args) #待测试
                else:
                    msg='{}({})已存在！'.format(anchor[1],args) #待测试
        else:
            status,username,liveroom=data_source.UserInfo(args)
            if(status==0):
                model.AddNewAnchor(args,username,liveroom)
                model.AddCard(args,id,is_group,liveroom)
                msg='{}({})添加成功！'.format(username,args) #待测试
            else:
                msg='{} UID不存在或网络错误！'.format(args)
    event.user.send_msg(msg)

removeuser = on_command('取关')
@removeuser.msg#取关主播
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：取关 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            status=model.DeleteCard(args,id,is_group)
            if status!=0:
                msg='{}({})不在当前群组/私聊关注列表'.format(anchor[1],args)
            else:
                msg='{}({})删除成功！'.format(anchor[1],args)
    event.user.send_msg(msg)

alllist = on_command('列表')
@alllist.msg#显示当前群聊/私聊中的关注列表
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg='主播名称(UID)\n'
    content=''
    anchor=model.GetAnchorList()
    for index in anchor:
        card=model.GetCard(index[0],id,is_group)
        if len(card)!=0:
            content+='{}({})\n{} {} {}\n'.format(index[1],index[0],str(card[2]).replace('1','动态:开').replace('0','动态:关'),str(card[3]).replace('1','直播:开').replace('0','直播:关'),str(card[4]).replace('1','全体成员:开').replace('0','全体成员:关'))
    if content=='':
        msg='当前群聊/私聊关注列表为空！'
    else:
        msg=msg+content
    event.user.send_msg(msg)

ondynamic = on_command('开启动态')
@ondynamic.msg#启动动态推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：开启动态 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                model.DynamicON(args,id,is_group)
                msg='{}({})开启动态推送！'.format(anchor[1],args)
    event.user.send_msg(msg)
offdynamic = on_command('关闭动态')
@offdynamic.msg#启动动态推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：关闭动态 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                model.DynamicOFF(args,id,is_group)
                msg='{}({})关闭动态推送！'.format(anchor[1],args)
    event.user.send_msg(msg)

onlive = on_command('开启直播')
@onlive.msg#启动直播推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：开启直播 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                if anchor[3]!=1:
                    msg='{}({})还未开启直播间！'.format(anchor[1],args)
                else:
                    model.LiveON(args,id,is_group)
                    msg='{}({})开启直播推送！'.format(anchor[1],args)
    event.user.send_msg(msg)

offlive = on_command('关闭直播')
@offlive.msg#启动直播推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：关闭直播 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                if anchor[3]!=1:
                    msg='{}({})还未开启直播间！'.format(anchor[1],args)
                else:
                    model.LiveOFF(args,id,is_group)
                    msg='{}({})关闭直播推送！'.format(anchor[1],args)
    event.user.send_msg(msg)

onat = on_command('开启全体')
@onat.msg#启动动态推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：开启全体 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                model.AtON(args,id,is_group)
                msg='{}({})开启直播@全体成员！'.format(anchor[1],args)
    event.user.send_msg(msg)

offat = on_command('关闭全体')
@offat.msg#启动动态推送
def handle(event,args):
    is_group=int(isGroup(event))
    if is_group:
        id=GetGroupName(event)
    else:
        id=GetFriendName(event)
    msg = '指令格式错误！请按照：关闭全体 UID'
    if args!='' and args.isdigit():
        anchor=model.GetAnchorInfo(args)
        if len(anchor)==0:
            msg = '{} 主播不存在！请检查UID是否错误'.format(args)
        else:
            card=model.GetCard(args,id,is_group)
            if len(card)==0:
                msg='{}({})不在当前群组/私聊关注列表！'.format(anchor[1],args)
            else:
                model.AtOFF(args,id,is_group)
                msg='{}({})关闭直播@全体成员！'.format(anchor[1],args)
    event.user.send_msg(msg)

help = on_command('帮助')
@help.msg#启动动态推送
def handle(event,args):
    menu='HanayoriBot(WeChat版)目前支持的功能：\n(请将UID替换为需操作的B站UID)\n关注 UID\n取关 UID\n列表\n开启动态 UID\n关闭动态 UID\n开启直播 UID\n关闭直播 UID\n开启全体 UID\n关闭全体 UID\n帮助\n'
    info='当前版本：v0.1\n作者：鹿乃ちゃんの猫\n反馈邮箱：kano@hanayori.top'
    msg=menu+info
    event.user.send_msg(msg)


