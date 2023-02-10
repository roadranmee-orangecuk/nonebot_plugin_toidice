# 技能检定指令
import re
import os
import random

from .dice import get_rd_result
from .playerc import show_playercharacter


def get_ra_result(text: str, group_id: str, user_id: str) -> dict | None:
    '''
    接口功能: 获取技能检定的结果信息。

    参数:

        text: str 去除指令文本后的用户纯文本信息。
        group_id: str 当前群号。
        user_id: str 用户qq号。

    返回值:

        : dict | None 包含数据和请求处理状态 status 的字典。
    '''
    if text == '':
        return None
    aname = re.findall(r'[^-+pb\d\s]+', text)[0]
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return {'status': 'USER_NOTFOUND'}
    datas = show_playercharacter(path_, aname, group_id)
    if datas is None:
        return {'status': 'CA_NOTFOUND'}
    avalue = datas['attrs'][aname]
    attr = re.findall(r'[^pb\s\d]+[-+\d]+', text)
    if len(attr) != 0:
        avalue_new = re.findall(r'[-+\d]+', attr[0])[0]
        if re.search(r'[-+]', avalue_new):
            avalue += int(avalue_new)
        else:
            avalue = int(avalue_new)
    pb = re.findall(r'[pb]+', text)
    if len(pb) == 0:
        text_pb = ''
    else:
        text_pb = pb[0]
    pb_result = get_pb(text_pb)
    rating = get_rating(avalue, pb_result['sum'])
    return {'process': pb_result['process'], 'sum': pb_result['sum'], 'avalue': avalue, 'rating': rating, 'status': 'RA_OK'}


def get_pb(text_pb: str) -> dict:
    '''
    (内部接口)
    接口功能: 获取可能包含惩罚奖励骰处理的掷骰信息。

    参数:

        text_pb: str 掷骰式中的惩罚奖励骰部分文本。

    返回值:

        : dict 包含掷骰过程 process 和结果值 sum 的字典。
    '''
    if text_pb == '':
        result = get_rd_result('1d100')
        return {'process': result['process'], 'sum': result['sum']}
    pbs = list(text_pb)
    pb_process = ''
    units = random.randint(0, 9)
    pb_sum = random.randint(0, 9)*10
    sum_ = if_sum_zero(pb_sum, units)
    for pb in pbs:
        dice = random.randint(0, 9)*10
        sum_now = if_sum_zero(dice, units)
        if pb == 'p':
            pb_process += 'p('+str(dice)+'|'+str(pb_sum)+')'
            if sum_now > sum_:
                pb_sum = dice
                sum_ = sum_now
        else:
            pb_process += 'b('+str(dice)+'|'+str(pb_sum)+')'
            if sum_now < sum_:
                pb_sum = dice
                sum_ = sum_now
    process = pb_process+'->'+str(pb_sum)+'+'+str(units)
    return {'process': process, 'sum': sum_}


def if_sum_zero(pb_sum: int, units: int):
    sum_ = pb_sum+units
    if sum_ == 0:
        sum_ = 100
    return sum_


def get_rating(avalue: int, sum_: int) -> str:
    '''
    (内部接口)
    接口功能: 获取检定评级。

    参数:

        avalue: int 属性值。
        sum_: int 结果值。

    返回值:

        : str 表示检定评级的字符串。
    '''
    if sum_ == 1:
        return 'BIG_SUCCESS'
    if sum_ == 100:
        return 'BIG_FAILURE'
    if sum_ <= avalue and sum_ > avalue/2:
        return 'SUCCESS'
    if sum_ <= avalue/2 and sum_ > avalue/5:
        return 'HARD_SUCCESS'
    if avalue >= 50:
        if sum_ > avalue:
            return 'FAILURE'
        if sum_ <= avalue/5 and sum_ > 5:
            return 'ULTIMATE_SUCCESS'
        if sum_ <= 5:
            return 'BIG_SUCCESS'
    else:
        if sum_ > avalue and sum_ <= 95:
            return 'FAILURE'
        if sum_ > 95:
            return 'BIG_FAILURE'
