# 调查员作成指令
from .dice import get_rd_result


def make_character_attributes() -> dict:
    '''
    接口功能: 生成调查员八大属性值和幸运值。

    参数:

        无。

    返回值:

        attrs: dict 包含生成的调查员八大属性值和幸运值的字典。
    '''
    str_result = get_rd_result('3d6')
    str_ = str_result['sum']*5      # 力量
    con_result = get_rd_result('3d6')
    con = con_result['sum']*5      # 体质
    siz_result = get_rd_result('2d6+6')
    siz = siz_result['sum']*5      # 体型
    dex_result = get_rd_result('3d6')
    dex = dex_result['sum']*5      # 敏捷
    app_result = get_rd_result('3d6')
    app = app_result['sum']*5      # 外貌
    int_result = get_rd_result('2d6+6')
    int_ = int_result['sum']*5      # 智力
    pow_result = get_rd_result('3d6')
    pow_ = pow_result['sum']*5      # 意志
    edu_result = get_rd_result('2d6+6')
    edu = edu_result['sum']*5      # 教育
    luk_result = get_rd_result('3d6')
    luk = luk_result['sum']*5      # 幸运
    sum_ = str_+con+siz+dex+app+int_+pow_+edu  # 不含幸运的属性值总和
    sum_luk = sum_+luk       # 含幸运的属性值总和
    attrs = {'str': str_, 'con': con, 'siz': siz, 'dex': dex, 'app': app, 'int': int_,
             'pow': pow_, 'edu': edu, 'luk': luk, 'sum': sum_, 'sum_luk': sum_luk}
    return attrs
