# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import redis_utils
from . import scu_session


async def handler_register(bot: nonebot.NoneBot, event: aiocqhttp.Event):
    # command parser
    if event.message[0]['type'] != 'text':
        return

    raw_message: str = event.message[0]['data']['text'].strip()
    message_split: list[str] = raw_message.split(' ')
    if len(message_split) != 2:
        return
    if message_split[0] not in ['绑定', 'bind']:
        return
    xk_token = message_split[1]
    qq_key = str(event.user_id)
    # save to redis
    await redis_utils.save_cookies(qq_key, {'XK_TOKEN': xk_token})
    await scu_session.add_session_dict(qq_key)
    success = await scu_session.session_login(qq_key)
    if success:
        await bot.send_private_msg(user_id=event.user_id, message='验证成功')
    else:
        await bot.send_private_msg(user_id=event.user_id, message='cookies无效')


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
    all_keys = redis_utils.get_all_keys()
    for qq_key in all_keys:
        await scu_session.session_login(qq_key)