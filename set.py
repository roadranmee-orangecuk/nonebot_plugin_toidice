# 设置属性指令
import re
import os
import json

commons = {
    '力量': ['str'], 'str': ['力量'],
    '敏捷': ['dex'], 'dex': ['敏捷'],
    '意志': ['pow', 'san', 'san值', '理智', '理智值'], 'pow': ['意志', 'san', 'san值', '理智', '理智值'],
    '体质': ['con'], 'con': ['体质'],
    '外貌': ['app'], 'app': ['外貌'],
    '教育': ['知识', 'edu'], '知识': ['教育', 'edu'], 'edu': ['教育', '知识'],
    '体型': ['siz'], 'siz': ['体型'],
    '智力': ['灵感', 'int'], '灵感': ['智力', 'int'], 'int': ['智力', '灵感'],
    'san': ['san值', '理智', '理智值'], 'san值': ['san', '理智', '理智值'], '理智': ['san', 'san值', '理智值'], '理智值': ['san', 'san值', '理智'],
    '幸运': ['运气'], '运气': ['幸运'],
    'mp': ['魔法'], '魔法': ['mp'],
    'hp': ['体力'], '体力': ['hp'],
    '计算机': ['计算机使用', '电脑'], '计算机使用': ['计算机', '电脑'], '电脑': ['计算机', '计算机使用'],
    '信用': ['信誉', '信用评级'], '信誉': ['信用', '信用评级'], '信用评级': ['信用', '信誉'],
    '克苏鲁': ['克苏鲁神话', 'cm'], '克苏鲁神话': ['克苏鲁', 'cm'], 'cm': ['克苏鲁', '克苏鲁神话'],
    '汽车': ['驾驶', '汽车驾驶'], '驾驶': ['汽车', '汽车驾驶'], '汽车驾驶': ['汽车', '驾驶'],
    '步枪': ['霰弹枪', '步霰'], '霰弹枪': ['步枪', '步霰'], '步霰': ['步枪', '霰弹枪'],
    '图书馆': ['图书馆使用'], '图书馆使用': ['图书馆'],
    '开锁': ['撬锁', '锁匠'], '撬锁': ['开锁', '锁匠'], '锁匠': ['开锁', '撬锁'],
    '博物学': ['自然学'], '自然学': ['博物学'],
    '领航': ['导航'], '导航': ['领航'],
    '重型操作': ['重型机械', '操作重型机械', '重型'], '重型机械': ['重型操作', '操作重型机械', '重型'], '操作重型机械': ['重型操作', '重型机械', '重型'], '重型': ['重型操作', '重型机械', '操作重型机械'],
}


def set_attributes(text: str, group_id: str, user_id: str) -> dict | None:
    '''
    接口功能: 设置角色卡属性。

    参数:

        text: str 去除指令文本后的用户纯文本信息。
        group_id: str 当前群号。
        user_id: str 用户qq号。

    返回值:
        : dict | None 包含数据和请求处理状态 status 的字典。
    '''
    attrs = re.findall(r'[\D]+[\d]+', text)
    if len(attrs) == 0:
        return None
    attrs_new = {}
    for attr in attrs:
        aname = re.findall(r'[^-+\d\s]+', attr)[0]
        avalue = re.findall(r'[-+\d]+', attr)[0]
        attrs_new[aname] = avalue
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return {'status': 'USER_NOTFOUND'}
    datas = get_playercharacter(path_, group_id)
    if datas is None:
        return {'status': 'PC_NOTFOUND'}
    pc = datas['pc']
    for kv in attrs_new.items():
        if re.search(r'[-+]', kv[1]):
            avalue_new = pc['attrs'][kv[0]]+int(kv[1])
            pc['attrs'][kv[0]] = avalue_new
        else:
            avalue_new = int(kv[1])
            pc['attrs'][kv[0]] = avalue_new
        if kv[0] in commons.keys():
            for key in commons[kv[0]]:
                pc['attrs'][key] = avalue_new
    with open(datas['path_pc'], 'w') as f:
        f.write(json.dumps(pc, ensure_ascii=False))
        f.close()
    return {'cname': datas['cname'], 'status': 'SET_OK'}


def get_playercharacter(path_: str, group_id: str) -> dict | None:
    '''
    (内部接口)
    接口功能: 获取角色卡信息。

    参数:

        path_: str 用户角色卡文件夹路径。
        group_id: str 当前群号。

    返回值:
        : dict | None 包含角色卡路径 path_pc 、角色卡名称 cname 和角色卡信息 pc 的字典。
    '''
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            try:
                if pc['groups'][group_id] == 1:
                    return {'path_pc': f'{path_}/{file}', 'cname': file.replace('.json', ''), 'pc': pc}
            except KeyError:
                continue
    return None
