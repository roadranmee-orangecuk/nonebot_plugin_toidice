# 设置调查员名称指令
import os
import json


def set_cname(text: str, group_id: str, user_id: str) -> dict | None:
    '''
    接口功能: 设置角色卡名称。

    参数:

        text: str 去除指令文本后的用户纯文本信息。
        group_id: str 当前群号。
        user_id: str 用户qq号。

    返回值:

        : dict | None 包含数据和请求处理状态 status 的字典。
    '''
    if text == '':
        return None
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return {'status': 'USER_NOTFOUND'}
    if os.path.exists(f'{path_}/{text}.json'):
        return {'status': 'PC_EXISTS'}
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            try:
                if pc['groups'][group_id] == 1:
                    os.rename(f'{path_}/{file}', f'{path_}/{text}.json')
                    return {'before': file.replace('.json', ''), 'now': text, 'status': 'SET_OK'}
            except KeyError:
                continue
    return {'status': 'PC_NOTFOUND'}
