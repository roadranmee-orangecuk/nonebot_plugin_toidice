# 秘密团分配预设背景指令
import random

MAX_COUNT = 10    # 玩家数量上限


def get_handout_assignments(text: str) -> list[dict[int, str]] | None:
    '''
    接口功能: 获取预设背景分配。

    参数:

        text: str 去除指令文本后的用户纯文本信息。

    返回值:

        assimts: list[dict[int, str] | None 包含预设背景分配信息的字典列表，字典元素中包含预设背景编号 order 和对应玩家名称 name 。
    '''
    players = text.split(' ')
    if text == '' or len(players) > MAX_COUNT:  # 超过玩家数量上限
        assimts = None
    else:
        # 生成与玩家列表一一对应的预设背景编号列表，例如：['张三', '李四', '王五']->[0,2,1]，表示ho1为张三，ho2为王五，ho3为李四
        orders = random.sample(range(0, len(players)), len(players))
        assimts = list(
            map(lambda x: {'order': x+1, 'name': players[orders[x]]}, range(0, len(players))))
    return assimts
