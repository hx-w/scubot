# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import redis_utils
from . import scu_session


async def handler_register(bot: nonebot.NoneBot, event: aiocqhttp.Event):
    # command parser
    if event.message[0]['type'] != 'text':
        return

    qq_key = str(event.user_id)

    raw_message: str = event.message[0]['data']['text'].strip()
    if 'route' not in raw_message: return
    cookies_dict = {}
    try:
        for line in raw_message.split(';'):
            key, value = line.split('=', 1)
            cookies_dict[key] = value
    except:
        return
    # save to redis
    await redis_utils.save_cookies(qq_key, cookies_dict)
    await scu_session.add_session_dict(qq_key)

    std_info = await scu_session.get_student_info(qq_key)
    if std_info == {}:
        await bot.send_private_msg(user_id=event.user_id, message='cookies无效')
        return
    std_name = std_info['xsInfoList'][0]['XM']
    std_id = std_info['xsInfoList'][0]['XH']
    success = await scu_session.get_student_picture(qq_key, str(std_id))
    if success:
        await bot.send_private_msg(user_id=event.user_id, message=f'{std_name} 你好\n' + nonebot.MessageSegment.image(file=f'file://{std_id}.jpg'))
    else:
        await bot.send_private_msg(user_id=event.user_id, message=f'{std_name} 你好')    

    # success = await scu_session.session_login(qq_key)
    # if success:
    #     await bot.send_private_msg(user_id=event.user_id, message='验证成功')
    #     std_info = await scu_session.session_student_info(qq_key)
    #     if std_info == {}: return
    #     course_list = await scu_session.session_course_list(qq_key)
    #     if course_list == {}: return
    #     message = f'{std_info["xs"]["XM"]} 你好\n\n你当前的选课有：'
    #     for course_ in course_list['xkjgList']:
    #         message += f'\n{course_["KCMC"]}({course_["RKJS"]})'
    #     await bot.send_private_msg(user_id=event.user_id, message=message)
    # else:
    #     await bot.send_private_msg(user_id=event.user_id, message='cookies无效')


async def handler_check(bot: nonebot.NoneBot, event: aiocqhttp.Event):
    # command parser
    if event.message[0]['type'] != 'text':
        return
    raw_message: str = event.message[0]['data']['text'].strip()
    if raw_message not in ['验证', 'verify', 'check']:
        return

    qq_key = str(event.user_id)
    spot, _ = await redis_utils.get_cookies(qq_key)
    if not spot:
        await bot.send_private_msg(user_id=event.user_id, message='请先输入： 绑定 <xk_token> 才可验证')
        return

    success = await scu_session.session_login(qq_key)
    if success:
        await bot.send_private_msg(user_id=event.user_id, message='验证成功')
    else:
        await bot.send_private_msg(user_id=event.user_id, message='cookies无效')


async def handler_check_all():
    all_keys = await redis_utils.get_all_keys()
    for qq_key in all_keys:
        await scu_session.session_login(qq_key)
