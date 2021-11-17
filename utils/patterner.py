COMMAND={}
class on_command():
    pattern=''
    def __init__(self,pattern) -> None:
        self.pattern=pattern
    def msg(self,func):
        if COMMAND.get(self.pattern)!=None:
            print('检测到冲突的规则：COMMAND:%s'%(self.pattern))
            raise Exception('插件加载失败！')
        def command(msg,args):
            print('匹配到规则：COMMAND:%s'%(self.pattern))
            func(msg,args)
        COMMAND[self.pattern]=command
        return command
