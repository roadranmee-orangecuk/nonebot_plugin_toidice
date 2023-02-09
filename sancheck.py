# 理智检定指令
import os

from .dice import get_rd_result
from .playerc import show_playercharacter
from .set import set_attributes


def get_sancheck(text: str, group_id: str, user_id: str):
    formulas = text.split('/')
    if len(formulas) != 2:
        return None
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return {'status': 'USER_NOTFOUND'}
    datas = show_playercharacter(path_, 'san', group_id)
    if datas is None:
        return {'status': 'CA_NOTFOUND'}
    avalue = datas['attrs']['san']
    ra_result = get_rd_result('1d100')
    if ra_result['sum'] > avalue:
        sc_result = get_rd_result(formulas[1])
        avalue -= sc_result['sum']
        set_attributes('san'+str(avalue), group_id, user_id)
        return {'text':formulas[1],'avalue': avalue, 'ra_sum': ra_result['sum'], 'sc_sum': sc_result['sum'], 'rating': 'FAILURE', 'status': 'SC_OK'}
    else:
        sc_result = get_rd_result(formulas[0])
        avalue -= sc_result['sum']
        set_attributes('san'+str(avalue), group_id, user_id)
        return {'text':formulas[0],'avalue': avalue, 'ra_sum': ra_result['sum'], 'sc_sum': sc_result['sum'], 'rating': 'SUCCESS', 'status': 'SC_OK'}
