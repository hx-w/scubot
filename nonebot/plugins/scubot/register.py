# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
import redis

from . import cookies


async def handler_register(bot: nonebot.NoneBot, redis_inst: redis.Redis, event: aiocqhttp.Event):
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
    # save to redis
    cookies.save_cookies(redis_inst, event.user_id, xk_token)
    await bot.send_private_msg(user_id=event.user_id, message="已保存cookies")
