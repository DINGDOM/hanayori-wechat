from . import matcher
from . import patterner
from . import library
from apscheduler.schedulers.background import BackgroundScheduler
scheduler=BackgroundScheduler()
pattern_command=matcher.pattern_command
on_command=patterner.on_command
isGroup=library.isGroup
GetFriendID=library.GetFriendID
GetGroupID=library.GetGroupID
GetFriendName=library.GetFriendName
GetGroupName=library.GetGroupName
At=library.At