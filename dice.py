# 普通掷骰指令
import random
import re

MAX_COUNT = 10  # 骰子数量上限


def get_rd_result(text: str) -> dict[str, int] | None:
    '''
    接口功能: 获取掷骰结果信息。

    参数:

        text: str 去除指令文本后的用户纯文本信息。

    返回值:

        result: dict[str, int] | None 包含用户请求的掷骰式 text 、掷骰过程 process 和结果值 sum 的字典。
    '''
    if text == '':
        text = '1d100'  # 无后缀的情况默认1d100
    ops_n_fs = get_operations_n_formulas(text)
    operations = ops_n_fs['operations']  # 加减运算符列表
    formulas = ops_n_fs['formulas']  # 不含加减运算符的掷骰子式列表
    sum_ = 0  # 结果值
    process = ''  # 掷骰过程
    i_op = 0    # 加减运算符列表指针
    for formula in formulas:
        process = get_process_start(process, operations, i_op)
        if re.search('d', formula):
            digs = formula.split('d', 1)
            count = get_count(digs[0])  # 骰子数
            sides = get_sides(digs[1])  # 面数
            if count == -1 or sides == -1:
                result = None
                return result
            for i in range(count):
                dice = random.sample(range(1, sides+1), 1)[0]
                sum_ = get_sum(sum_, operations, i_op, dice)
                process += str(dice)+'+'
            process = process[:-1]
        else:   # 子式中不存在d运算符，考虑子式为简单数字的情况
            num = get_num(formula)
            if num == -1:
                result = None
                return result
            sum_ = get_sum(sum_, operations, i_op, num)
            process += str(num)
        process += ')'
        i_op += 1
    result = {'text': text, 'process': process, 'sum': sum_}
    return result


def get_operations_n_formulas(text: str) -> dict[list]:
    '''
    (内部接口)
    接口功能: 获取加减运算符列表和掷骰子式列表。

    参数:

        text: str 去除指令文本后的用户纯文本信息。

    返回值:

        ops_n_fs: dict[list] 包含加减运算符列表和掷骰子式列表的字典。
    '''
    if re.search('[+]', text) or re.search('-', text):
        operations = []  # 加减运算符列表，加号为0，减号为1
        formulas = text.split('+')
        i_op = 0
        for formula in formulas:
            operations.append(0)    # 第一个式子默认为加
            if re.search('-', text):
                for i in range(formula.count('-')):
                    # 算出减号个数，在当前元素后插入减号数量的1
                    operations.insert(i_op+i+1, 1)
            i_op += 1
        formulas = re.split('[+-]', text)   # 重新将掷骰式分割为没有加减运算的掷骰子式列表
    else:
        operations = [0]    # 掷骰式里没有加减运算，默认为加
        formulas = [text]
    ops_n_fs = {'operations': operations, 'formulas': formulas}
    return ops_n_fs


def get_sum(sum_: int, operations: list[int], i_op: int, dice: int) -> int:
    '''
    (内部接口)
    接口功能: 获取运算后的结果值。

    参数:

        sum_: int 运算前的结果值。
        operations: list[int] 加减运算符列表。
        i_op: int 加减运算符列表指针。
        dice: int 当前掷骰子式的掷骰结果。

    返回值:

        sum_: int 运算后的结果值。
    '''
    if operations[i_op] == 0:
        sum_ += dice    # 对应加减运算符为0，为加法
    else:
        sum_ -= dice    # 对应加减运算符为1，为减法
    return sum_


def get_process_start(process: str, operations: list[int], i_op: int) -> str:
    '''
    (内部接口)
    接口功能: 获取当前掷骰子式的掷骰过程起始符，一个完整掷骰子式的掷骰过程例如(1+2+3)、+(3+4+5)、-(6+7+8)，起始符分别为(、+(、-(。

    参数:

        process: str 当前的掷骰过程。
        operations: list[int] 加减运算符列表。
        i_op: int 加减运算符列表指针。

    返回值:

        process: str 添加了起始符后的掷骰过程。
    '''
    if operations[i_op] == 0:
        if i_op == 0:
            process += '('  # 对应加减运算符为0，且加减运算符列表指针为0，说明为第一个子式
        else:
            process += '+('
    else:
        process += '-('
    return process


def get_count(dig: str) -> int:
    '''
    (内部接口)
    接口功能: 获取骰子数，返回值为-1时表示不合法。

    参数:

        dig: str 表示骰子数的字符（串）。

    返回值:

        count: int 骰子数。
    '''
    if dig == '':
        count = 1  # 符合简易公式dy的情况，骰子数作1处理
    else:
        try:
            count = int(dig)
        except ValueError:
            count = -1  # 字符不合法
    if count < 1 or count > MAX_COUNT:
        count = -1  # 骰子数不合法或超出骰子数上限
    return count


def get_sides(dig: str) -> int:
    '''
    (内部接口)
    接口功能: 获取面数，返回值为-1时表示不合法。

    参数:

        dig: str 表示面数的字符（串）。

    返回值:

        sides: int 面数。
    '''
    try:
        sides = int(dig)
    except ValueError:
        sides = -1
    return sides


def get_num(formula: str) -> int:
    '''
    (内部接口)
    接口功能: 获取简单数字的值，返回值为-1时表示不合法。

    参数:

        dig: str 表示简单数字的字符（串）。

    返回值:

        sides: int 简单数字的值。
    '''
    try:
        num = int(formula)
    except ValueError:
        num = -1
    return num
