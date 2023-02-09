# 观察队列管理指令
import os
import json


def manage_observes(text: str, group_id: str, user_id: str, nickname: str) -> dict | None:
    '''
    接口功能: 管理观察队列。

    参数:

        text: str 去除指令文本后的用户纯文本信息。

        group_id: str 当前群号。

        user_id: str 用户qq号。

        nickname: str 用户昵称，在这里为当前群组下用户的备注。

    返回值:

        : dict | None 包含请求处理状态 status 的字典，例如值为'JOIN_OK'时表示成功加入观察队列，为'USER_EXISTS'时表示用户已在观察队列中。
    '''
    path_ = f'data/toidice/groups/{group_id}/obs.json'
    if not os.path.exists(path_):   # 初始化当前群组观察队列json文件
        os.makedirs(f'data/toidice/groups/{group_id}')
        with open(path_, 'w') as f:
            f.write('{}')
            f.close()
    if text == '':  # 加入观察队列
        if join_observes(path_, user_id, nickname) is False:
            return {'status': 'USER_EXISTS'}
        return {'status': 'JOIN_OK'}
    elif text == 'exit':  # 退出观察队列
        if exit_observes(path_, user_id) is False:
            return {'status': 'USER_NOTFOUND'}
        return {'status': 'EXIT_OK'}
    elif text == 'list':  # 查看观察队列
        with open(path_, 'r') as f:
            obs = json.load(f)
            f.close()
        return {'observes': obs, 'status': 'LIST_OK'}
    elif text == 'clr':  # 清空观察队列
        with open(path_, 'w') as f:
            f.write('{}')
            f.close()
        return {'status': 'CLEAR_OK'}
    else:
        return None


def join_observes(path_: str, user_id: str, nickname: str) -> bool:
    '''
    (内部接口)
    接口功能: 处理加入观察队列的请求。

    参数:

        path_: str 当前群组观察队列json文件路径。

        user_id: str 用户qq号。

        nickname: str 用户昵称，在这里为当前群组下用户的备注。

    返回值:

        : bool 
    '''
    with open(path_, 'r') as f:
        obs = json.load(f)
        if user_id in obs.keys():
            f.close()
            return False
        f.close()
    obs[user_id] = nickname
    with open(path_, 'w') as f:
        f.write(json.dumps(obs, ensure_ascii=False))
        f.close()
    return True


def exit_observes(path_: str, user_id: str) -> bool:
    '''
    (内部接口)
    接口功能: 处理退出观察队列的请求。

    参数:

        path_: str 当前群组观察队列json文件路径。

        user_id: str 用户qq号。

    返回值:

        : bool 
    '''
    with open(path_, 'r') as f:
        obs = json.load(f)
        if user_id not in obs.keys():
            f.close()
            return False
        f.close()
    del obs[user_id]
    with open(path_, 'w') as f:
        f.write(json.dumps(obs, ensure_ascii=False))
        f.close()
    return True
