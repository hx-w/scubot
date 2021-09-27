# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
import redis

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()
redis_inst: redis.Redis = None

@nonebot.on_websocket_connect
async def on_connect(event: aiocqhttp.Event):
    global redis_inst
    redis_inst = redis.Redis(host='redis', port=6379, decode_responses=True)
    print(f'[on_websocket_connect] {redis_inst}')


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, redis_inst, event)
