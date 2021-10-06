# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, event)
    await register.handler_check(bot, event)
