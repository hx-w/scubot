# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot
from quart import request

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, event)

@bot.asgi.route('/query_log')
async def query_code():
    code = request.args.get('code','')
    return code