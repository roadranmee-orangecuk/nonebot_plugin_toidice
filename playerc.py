# 角色卡管理指令
import re
import os
import random
import string
import json


def manage_playercharacters(text: str, group_id: str, user_id: str) -> dict | None:
    '''
    接口功能: 管理角色卡。

    参数:

        text: str 去除指令文本后的用户纯文本信息。
        group_id: str 当前群号。
        user_id: str 用户qq号。

    返回值:

        : dict | None 包含数据和请求处理状态 status 的字典。
    '''
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        os.makedirs(path_)
    if text == '':
        cancel_character_bind(path_, group_id)  # 创建前先解除该群组原有的调查员绑定
        return {'cname': create_playercharacter(path_, ''.join(random.sample(string.ascii_letters, 6)), group_id), 'status': 'CREATE_OK'}
    elif re.search('^show.*', text):
        commands = ['show ', 'show']
        for command in commands:
            text = text.replace(command, '')
        attrs = text
        datas = show_playercharacter(path_, attrs, group_id)
        if datas is not None:
            return {'cname': datas['cname'], 'attrs': datas['attrs'], 'status': 'SHOW_OK'}
        else:
            return {'status': 'CA_NOTFOUND'}
    elif text == 'list':
        return {'pcs': playercharacters_list(path_), 'status': 'LIST_OK'}
    else:
        cancel_character_bind(path_, group_id)
        if not os.path.exists(f'{path_}/{text}.json'):
            # 若调查员不存在，创建一个为该名称的调查员
            return {'cname': create_playercharacter(path_, text, group_id), 'status': 'CREATE_OK'}
        switch_playercharacter(path_, group_id, text)   # 若调查员存在，则切换绑定该调查员
        return {'cname': text, 'status': 'SWITCH_OK'}


def create_playercharacter(path_: str, cname: str, group_id: str) -> str:
    '''
    (内部接口)
    接口功能: 创建角色卡。

    参数:

        path_: str 用户角色卡文件夹路径。
        cname: str 角色卡名称。
        group_id: str 当前群号。

    返回值:

        cname: str 角色卡名称。
    '''
    groups = {}
    groups[group_id] = 1
    pc = {'groups': groups, 'attrs': {'力量': 0, 'str': 0, '敏捷': 0, 'dex': 0, '意志': 0, 'pow': 0, '体质': 0, 'con': 0, '外貌': 0, 'app': 0, '教育': 0, '知识': 0, 'edu': 0, '体型': 0, 'siz': 0, '智力': 0, '灵感': 0, 'int': 0, 'san': 0, 'san值': 0, '理智': 0, '理智值': 0, '幸运': 0, '运气': 0, 'mp': 0, '魔法': 0, 'hp': 0, '体力': 0, '会计': 5, '人类学': 1, '估价': 5, '考古学': 1, '取悦': 15, '攀爬': 20, '计算机': 5, '计算机使用': 5, '电脑': 5, '信用': 0, '信誉': 0, '信用评级': 0, '克苏鲁': 0, '克苏鲁神话': 0, 'cm': 0, '乔装': 5, '闪避': 0, '汽车': 20,
                                      '驾驶': 20, '汽车驾驶': 20, '电气维修': 10, '电子学': 1, '话术': 5, '斗殴': 25, '手枪': 20, '急救': 30, '历史': 5, '恐吓': 15, '跳跃': 20, '母语': 0, '法律': 5, '图书馆': 20, '图书馆使用': 20, '聆听': 20, '开锁': 1, '撬锁': 1, '锁匠': 1, '机械维修': 10, '医学': 1, '博物学': 10, '自然学': 10, '领航': 10, '导航': 10, '神秘学': 5, '重型操作': 1, '重型机械': 1, '操作重型机械': 1, '重型': 1, '说服': 10, '精神分析': 1, '心理学': 10, '骑术': 5, '妙手': 10, '侦查': 25, '潜行': 20, '生存': 10, '游泳': 20, '投掷': 20, '追踪': 10, '驯兽': 5, '潜水': 1, '爆破': 1, '读唇': 1, '催眠': 1, '炮术': 1}}
    with open(f'{path_}/{cname}.json', 'w') as f:
        f.write(json.dumps(pc, ensure_ascii=False))
        f.close()
    return cname


def show_playercharacter(path_: str, attrs: str, group_id: str) -> dict | None:
    '''
    (内部接口)
    接口功能: 查看当前群组绑定角色卡属性。

    参数:

        path_: str 用户角色卡文件夹路径。
        attrs: str 属性名称。
        group_id: str 当前群号。

    返回值:

        : dict | None 角色卡名称 cname 和包含角色卡属性的字典 attrs 。
    '''
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            try:
                if pc['groups'][group_id] == 1:
                    if attrs == '':
                        return {'cname': file.replace('.json', ''), 'attrs': pc['attrs']}
                    else:
                        return {'cname': file.replace('.json', ''), 'attrs': {attrs: pc['attrs'][attrs]}}
            except KeyError:
                continue
    return None


def playercharacters_list(path_: str) -> list[dict]:
    '''
    (内部接口)
    接口功能: 查看用户自己的角色卡列表。

    参数:

        path_: str 用户角色卡文件夹路径。

    返回值:

        pcs: list[dict] 角色卡名称 cname 和绑定群组 groups 组成的字典列表。
    '''
    pcs = []
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            pcs.append({'cname': file.replace(
                '.json', ''), 'groups': pc['groups']})
    return pcs


def switch_playercharacter(path_: str, group_id: str, cname: str):
    '''
    (内部接口)
    接口功能: 切换绑定角色卡。

    参数:

        path_: str 用户角色卡文件夹路径。
        group_id: str 当前群号。
        cname: str 角色卡名称。

    返回值:

        : None
    '''
    with open(f'{path_}/{cname}.json', 'r') as f:
        pc = json.load(f)
        f.close()
    pc['groups'][group_id] = 1
    with open(f'{path_}/{cname}.json', 'w') as f:
        f.write(json.dumps(pc, ensure_ascii=False))
        f.close()
    return


def cancel_character_bind(path_: str, group_id: str) -> None:
    '''
    (内部接口)
    接口功能: 取消用户当前群组的角色卡绑定。

    参数:

        path_: str 用户角色卡文件夹路径。
        group_id: str 当前群号。

    返回值:

        : None
    '''
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            try:
                if pc['groups'][group_id] == 1:
                    del pc['groups'][group_id]
                    with open(f'{path_}/{file}', 'w') as f:
                        f.write(json.dumps(pc, ensure_ascii=False))
                        f.close()
            except KeyError:
                continue
    return
