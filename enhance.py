# 属性成长检定指令
import os

from .dice import get_rd_result
from .playerc import show_playercharacter
from .set import set_attributes


def enhance_attribute(text: str, group_id: str, user_id: str):
    aname = text
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return {'status': 'USER_NOTFOUND'}
    datas = show_playercharacter(path_, aname, group_id)
    if datas is None:
        return {'status': 'CA_NOTFOUND'}
    avalue = datas['attrs'][aname]
    ra_result = get_rd_result('1d100')
    if ra_result['sum'] > avalue:
        en_result = get_rd_result('1d10')
        avalue += en_result['sum']
        set_attributes(aname+str(avalue), group_id, user_id)
        return {'aname': aname, 'avalue': avalue, 'ra_sum': ra_result['sum'], 'en_sum': en_result['sum'], 'rating': 'SUCCESS', 'status': 'EN_OK'}
    return {'aname': aname, 'avalue': avalue, 'ra_sum': ra_result['sum'], 'rating': 'FAILURE', 'status': 'EN_OK'}
