import os
import json

from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from nonebot.adapters.onebot.v11.message import Message

from .config import init_reply
from .dice import get_rd_result
from .rollattr import get_ra_result
from .sancheck import get_sancheck
from .enhance import enhance_attribute
from .createoc import make_character_attributes
from .playerc import manage_playercharacters
from .set import set_attributes
from .cname import set_cname
from .observe import manage_observes
from .handout import get_handout_assignments
from .help import get_tip

rd = on_keyword(['.r', '。r'], priority=2)  # 普通掷骰
ra = on_keyword(['.ra', '。ra'], priority=1)    # 技能检定
rh = on_keyword(['.rh', '。rh'], priority=1)    # 暗骰
sc = on_keyword(['.sc', '。sc'], priority=1)    # 理智检定
en = on_keyword(['.en', '。en'], priority=1)  # 属性成长检定
coc = on_keyword(['.coc', '。coc'], priority=1)  # 调查员作成
pc = on_keyword(['.pc', '。pc'], priority=1)    # 调查员角色卡管理
st = on_keyword(['.st', '。st'], priority=1)    # 设置属性
cn = on_keyword(['.cn', '。cn'], priority=1)    # 设置调查员名称
ob = on_keyword(['.ob', '。ob'], priority=1)    # 观察队列管理
ho = on_keyword(['.ho', '。ho'], priority=1)    # 预设背景分配


def get_user_defined_reply() -> dict[str, str]:
    path_ = 'data/toidice/config'
    if not os.path.exists(path_):
        os.makedirs(path_)
    if not os.path.exists(f'{path_}/UserDefinedReply.json'):
        with open(f'{path_}/UserDefinedReply.json', 'w') as f:
            f.write(json.dumps(init_reply(), ensure_ascii=False))
            f.close()
    with open(f'{path_}/UserDefinedReply.json', 'r') as f:
        reply = json.load(f)
        f.close()
    return reply


def get_message_id(event_description: str) -> str:
    message_id = event_description.split(' ')[1]
    return message_id


async def get_nickname(bot: Bot, message_id: str) -> str:
    datas = await bot.call_api('get_msg', **{'message_id': message_id})
    nickname = datas['sender']['nickname']
    if 'group_id' not in datas.keys():
        return nickname
    group_id = str(datas['group_id'])
    user_id = str(datas['sender']['user_id'])
    path_ = f'data/toidice/users/{user_id}'
    if not os.path.exists(path_):
        return nickname
    for root, dirs, files in os.walk(path_):
        for file in files:
            with open(f'{path_}/{file}', 'r') as f:
                pc = json.load(f)
                f.close()
            try:
                if pc['groups'][group_id] == 1:
                    nickname = file.replace('.json', '')
                    return nickname
            except KeyError:
                continue
    return nickname


def get_group_id(session_id: str) -> str:
    group_id = session_id.split('_')[1]
    return group_id


async def get_group_name(bot: Bot, group_id: str) -> str:
    data = await bot.call_api('get_group_info', **{'group_id': group_id})
    group_name = data['group_name']
    return group_name


@rd.handle()
async def _(bot: Bot, event: Event):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.r', '。r']
    for command in commands:
        text = text.replace(command, '')
    result = get_rd_result(text)
    if result is not None:
        text = result['text']   # 掷骰式
        process = result['process']   # 掷骰过程
        sum_ = result['sum']  # 结果值
        nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
        content = reply['r'].format(nickname, text, process, sum_)
    else:
        content = get_tip('rd')+'\n\n'+get_tip('ps')
    await rd.finish(Message(content))


@ra.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.ra ', '。ra ', '.ra', '。ra']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = get_ra_result(text, group_id, event.get_user_id())
    if result is None:
        content = get_tip('ra')+'\n\n'+get_tip('ps')
    elif result['status'] == 'USER_NOTFOUND':
        content = reply['ra_user_notfound'].format(nickname)
    elif result['status'] == 'CA_NOTFOUND':
        content = reply['ra_ca_notfound'].format(nickname)
    elif result['status'] == 'RA_OK':
        process = result['process']  # 掷骰过程
        sum_ = result['sum']    # 结果值
        avalue = result['avalue']   # 属性值
        rating = result['rating']   # 检定评级
        if rating == 'BIG_SUCCESS':
            content = reply['big_success'].format(
                nickname, text, process, sum_, avalue)
        elif rating == 'ULTIMATE_SUCCESS':
            content = reply['ultimate_success'].format(
                nickname, text, process, sum_, avalue)
        elif rating == 'HARD_SUCCESS':
            content = reply['hard_success'].format(
                nickname, text, process, sum_, avalue)
        elif rating == 'SUCCESS':
            content = reply['success'].format(
                nickname, text, process, sum_, avalue)
        elif rating == 'FAILURE':
            content = reply['failure'].format(
                nickname, text, process, sum_, avalue)
        elif rating == 'BIG_FAILURE':
            content = reply['big_failure'].format(
                nickname, text, process, sum_, avalue)
    await ra.finish(Message(content))


@rh.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.rh', '。rh']
    for command in commands:
        text = text.replace(command, '')
    result = get_rd_result(text)
    if result is not None:
        text = result['text']
        proccess = result['process']
        sum_ = result['sum']
        group_id = get_group_id(event.get_session_id())
        group_name = await get_group_name(bot, group_id)
        nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
        content_private = reply['rh_private'].format(
            group_name, group_id, nickname, text, proccess, sum_)
        await bot.call_api('send_private_msg', **{'user_id': event.get_user_id(), 'group_id': group_id, 'message': content_private})
        content = reply['rh_group'].format(nickname)
        path_ = f'data/toidice/groups/{group_id}/obs.json'
        if os.path.exists(path_):
            with open(path_, 'r') as f:
                observes = list(json.load(f).keys())
                count = len(observes)
                f.close()
            if count != 0:
                await send_obs_msg(1, count, group_id, content_private, observes, bot)
    else:
        content = get_tip('rh')+'\n\n'+get_tip('ps')
    await rh.finish(Message(content))


async def send_obs_msg(order: int, count: int, group_id: str, content_private: str, observes: list[str], bot: Bot):
    if order < count:
        await send_obs_msg(order+1, count, group_id, content_private, observes, bot)
    await bot.call_api('send_private_msg', **{'user_id': observes[order-1], 'group_id': group_id, 'message': content_private})


@sc.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.en ', '。en ', '.en', '。en']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = get_sancheck(text, group_id, event.get_user_id())
    if result is None:
        content = get_tip('sc')+'\n\n'+get_tip('ps')
    elif result['status'] == 'USER_NOTFOUND':
        content = reply['sc_user_notfound'].format(nickname)
    elif result['status'] == 'CA_NOTFOUND':
        content = reply['sc_ca_notfound'].format(nickname)
    elif result['status'] == 'SC_OK':
        text_sc = result['text']
        avalue = result['avalue']
        ra_sum = result['ra_sum']
        sc_sum = result['sc_sum']
        if result['rating'] == 'SUCCESS':
            content = reply['sc_success'].format(
                nickname, avalue+sc_sum, avalue, ra_sum, sc_sum, text_sc)
        else:
            content = reply['sc_failure'].format(
                nickname, avalue+sc_sum, avalue, ra_sum, sc_sum, text_sc)
    await sc.finish(Message(content))


@en.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.en ', '。en ', '.en', '。en']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = enhance_attribute(text, group_id, event.get_user_id())
    if result['status'] == 'USER_NOTFOUND':
        content = reply['en_user_notfound'].format(nickname)
    elif result['status'] == 'CA_NOTFOUND':
        content = reply['en_ca_notfound'].format(nickname)
    elif result['status'] == 'EN_OK':
        aname = result['aname']
        avalue = result['avalue']
        ra_sum = result['ra_sum']
        if result['rating'] == 'SUCCESS':
            en_sum = result['en_sum']
            content = reply['en_success'].format(nickname,
                                                 aname, avalue-en_sum, ra_sum, en_sum, avalue)
        else:
            content = reply['en_failure'].format(
                nickname, aname, avalue, ra_sum)
    await en.finish(Message(content))


@coc.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    MAX_COUNT = 10    # 作成调查员数量上限
    text = event.get_plaintext()
    commands = ['.coc ', '。coc ', '.coc', '。coc']
    for command in commands:
        text = text.replace(command, '')
    try:
        if text == '':
            count = 1  # 作成调查员个数，默认为1
        else:
            count = int(text)
        if count > MAX_COUNT:
            content = get_tip('coc')+'\n\n'+get_tip('ps')
            await coc.finish(Message(content))
        else:
            await send_oc_msg(1, count, bot, event)
            await coc.finish()
    except ValueError:
        content = get_tip('coc')+'\n\n'+get_tip('ps')
        await coc.finish(Message(content))


async def send_oc_msg(order: int, count: int, bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    attrs = make_character_attributes()
    str_ = str(attrs['str'])    # 力量
    con = str(attrs['con'])  # 体质
    siz = str(attrs['siz'])  # 体型
    dex = str(attrs['dex'])  # 敏捷
    app = str(attrs['app'])  # 外貌
    int_ = str(attrs['int'])  # 智力
    pow_ = str(attrs['pow'])  # 意志
    edu = str(attrs['edu'])  # 教育
    luk = str(attrs['luk'])  # 幸运
    sum_ = str(attrs['sum'])  # 不含幸运的属性值总和
    sum_luk = str(attrs['sum_luk'])  # 含幸运的属性值总和
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    content = reply['coc'].format(
        nickname, str_, con, siz, dex, app, int_, pow_, edu, luk, sum_, sum_luk)
    if order < count:
        await send_oc_msg(order+1, count, bot, event)
    await coc.send(Message(content))


@pc.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.pc ', '。pc ', '.pc', '。pc']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = manage_playercharacters(text, group_id, event.get_user_id())
    if result['status'] == 'CREATE_OK':  # 创建调查员
        cname = result['cname']  # 调查员名称
        content = reply['pc_create_ok'].format(nickname, cname)
    elif result['status'] == 'SHOW_OK':  # 查看当前群组绑定调查员
        cname = result['cname']
        attrs = result['attrs']  # 调查员属性
        content = reply['pc_show_ok'].format(cname)
        for kv in attrs.items():
            aname = kv[0]   # 属性名称
            avalue = kv[1]  # 属性值
            content += f'{aname}{avalue}'
    elif result['status'] == 'CA_NOTFOUND':
        content = reply['pc_ca_notfound'].format(nickname)
    elif result['status'] == 'LIST_OK':  # 查看调查员列表
        content = reply['pc_list_ok'].format(nickname)
        pcs = result['pcs']
        for pc_ in pcs:
            cname = pc_['cname']
            groups = pc_['groups']
            content += f'{cname}('
            for kv in groups.items():
                group = kv[0]
                content += f'{group} '
            content += ')\n'
    elif result['status'] == 'SWITCH_OK':   # 切换调查员
        cname = result['cname']
        content = reply['pc_switch_ok'].format(cname)
    await pc.finish(Message(content))


@st.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.st ', '。st ', '.st', '。st']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = set_attributes(text, group_id, event.get_user_id())
    if result is None:
        content = get_tip('st')+'\n\n'+get_tip('ps')
    elif result['status'] == 'USER_NOTFOUND':
        content = reply['st_user_notfound'].format(nickname)
    elif result['status'] == 'PC_NOTFOUND':
        content = reply['st_pc_notfound'].format(nickname)
    elif result['status'] == 'SET_OK':
        cname = result['cname']
        content = reply['st_set_ok'].format(cname)
    await st.finish(Message(content))


@cn.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.cn ', '。cn ', '.cn', '。cn']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = set_cname(text, group_id, event.get_user_id())
    if result is None:
        content = get_tip('cn')+'\n\n'+get_tip('ps')
    elif result['status'] == 'USER_NOTFOUND':
        content = reply['cn_user_notfound'].format(nickname)
    elif result['status'] == 'PC_NOTFOUND':
        content = reply['cn_pc_notfound'].format(nickname)
    elif result['status'] == 'PC_EXISTS':
        content = reply['cn_pc_exists'].format(text)
    elif result['status'] == 'SET_OK':
        before = result['before']   # 原角色卡名称
        now = result['now']  # 新角色卡名称
        content = reply['cn_set_ok'].format(before, now)
    await cn.finish(Message(content))


@ob.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.ob ', '。ob ', '.ob', '。ob']
    for command in commands:
        text = text.replace(command, '')
    group_id = get_group_id(event.get_session_id())
    nickname = await get_nickname(bot, get_message_id(event.get_event_description()))
    result = manage_observes(text, group_id, event.get_user_id(), nickname)
    if result is None:
        content = get_tip('ob')+'\n\n'+get_tip('ps')
    elif result['status'] == 'JOIN_OK':
        content = reply['ob_join_ok'].format(nickname)
    elif result['status'] == 'USER_EXISTS':
        content = reply['ob_user_exists'].format(nickname)
    elif result['status'] == 'EXIT_OK':
        content = reply['ob_exit_ok'].format(nickname)
    elif result['status'] == 'USER_NOTFOUND':
        content = reply['ob_user_notfound'].format(nickname)
    elif result['status'] == 'LIST_OK':
        content = reply['ob_list_ok']
        for key, value in result['observes'].items():   # 用户qq号和用户昵称
            content += f'{value}({key})\n'
    elif result['status'] == 'CLEAR_OK':
        content = reply['ob_clear_ok']
    await ob.finish(Message(content))


@ho.handle()
async def _(event: Event):
    reply = get_user_defined_reply()
    text = event.get_plaintext()
    commands = ['.ho ', '。ho ', '.ho', '。ho']
    for command in commands:
        text = text.replace(command, '')
    content = reply['ho']
    assimts = get_handout_assignments(text)
    if assimts is not None:
        for assimt in assimts:
            order = str(assimt['order'])    # 预设背景编号
            name = assimt['name']   # 玩家名称
            content += f'ho{order}：{name}\n'
    else:
        content = get_tip('ho')+'\n\n'+get_tip('ps')
    await ho.finish(Message(content))
