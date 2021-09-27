# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
import redis

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()
redis_inst: redis.Redis = redis.Redis(
    host='redis', port=6379, decode_responses=True)


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, redis_inst, event)
