######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : utils
# @created     : 星期二 12月 07, 2021 20:28:55 CST
#
# @description : 
######################################################################



class DongTaiAppConfigPatch():
    def ready(self):
        try:
            from plugin import monkey_patch
            print(self.name)
            monkey_patch(self.name)
        except ImportError as e:
            print('No monkey_patch found')
