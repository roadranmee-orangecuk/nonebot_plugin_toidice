# 帮助指令
tips = {
    'r': '.r[f1, n1][+, -][f2, n2][+, -][f3, n3][+, -]...\n\nr：普通掷骰指令；\nf(1, 2, 3, ...)：满足 xdy 形式或 dy 简易形式、不存在加减运算的掷骰子式，如 4d6 、 d100 ，骰子数量上限默认为 10 ，未填写默认为 1d100 ；\nn(1, 2, 3, ...)：简单的数字',
    'rd': '.r[f1, n1][+, -][f2, n2][+, -][f3, n3][+, -]...\n\nr：普通掷骰指令；\nf(1, 2, 3, ...)：满足 xdy 形式或 dy 简易形式、不存在加减运算的掷骰子式，如 4d6 、 d100 ，骰子数量上限默认为 10 ，未填写默认为 1d100 ；\nn(1, 2, 3, ...)：简单的数字',
    'ra': '.ra([pb])n(([-+])v)\n\nra：技能检定指令；\np：惩罚骰；\nb：奖励骰， p 和 b 的数量分别表示惩罚骰和奖励骰的数量；\nn：属性名称；\nv：属性值或属性调整值，未填写默认为当前群组绑定角色卡属性值',
    'rh': '.rh[f1, n1][+, -][f2, n2][+, -][f3, n3][+, -]...\n\nrh：暗骰指令',
    'sc': '.sc sf/ff\n\nsc：理智检定指令；\nsf：成功时掷骰式；\nff：失败时掷骰式',
    'en': '.en n\n\nen：属性成长检定指令；\nn：属性名称',
    'coc': '.coc n\n\ncoc：调查员作成指令；\nn：作成调查员数量，上限默认为 10 ，未填写默认为 1 ',
    'pc': '.pc[show (attr), list, (cn)]\n\npc：角色卡管理指令；\nshow：查看当前群组绑定角色卡属性；\nattr：属性名称，省略时默认查看所有属性；\nlist：查看用户自己的角色卡列表；\ncn：角色卡名称，省略时默认创建一个名称为六位字母的角色卡，若角色卡已存在则切换，不存在则创建一个指定名称的角色卡',
    'st': '.st n1([-+])v1n2([-+])v2n3([-+])v3...\n\nst：设置属性指令；\nn(1, 2, 3, ...)：属性名称；\nv(1, 2, 3, ...)：属性值或属性调整值',
    'cn': '.cn n\n\ncn：设置角色卡名称指令；\nn：新的角色卡名称',
    'ob': '.ob[exit, list, clr]\n\nob：观察队列管理指令，无后缀默认为加入观察队列；\nexit：退出观察队列；\nlist：查看观察队列；\nclr：清除观察队列',
    'ho': '.ho pl1 pl2 pl3 ...\n\nho：秘密团分配预设背景指令；\npl[1, 2, 3, ...]：设定参与分配玩家的名称，玩家数量上限默认为 10 ',
    'ps': '使用 .help 指令查看更多的 toidice 帮助内容'
}

theme ='''
欢迎使用toidice(Alpha)！
这是一款基于nonebot2和go-cqhttp的coc7th跑团插件
git:https://github.com/roadranmee-orangecuk/nonebot_plugin_toidice
目前正常运行的指令集：
    r:  普通掷骰
    ra: 技能检定
    rh: 暗骰
    sc: 理智检定
    en: 属性成长检定
    coc:调查员作成
    pc: 角色卡管理
    st: 设置属性
    cn: 设置角色卡名称
    ob: 观察队列管理
    ho: 秘密团分配预设背景
使用 .help 指令名 查看指令具体使用提示
有更多问题请提交issue或联系开发者QQ:1289468324
'''


def get_help(text: str):
    if text == '':
        return theme
    try:
        help_ = tips[text]
    except KeyError:
        return None
    return help_


def get_tip(command: str) -> dict[str] | None:
    '''
    接口功能: 获取指令对应提示。

    参数：

        command: str 指令文本。

    返回值：

        tip: dict[str] | None 指令对应提示。
    '''
    tip = tips[command]
    return tip
