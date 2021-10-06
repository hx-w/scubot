# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, event)


@nonebot.on_request('friend')
async def _(session: nonebot.RequestSession):
    if '7355608' in session.event.comment:
        await session.approve()
        return
    await session.reject('验证失败')


@nonebot.scheduler.scheduled_job('cron', hours=7, jitter=120)
async def handler_timer():
    all_config = await register.get_all_config()
    # debug
    await bot.send_private_msg(user_id=765892480, message=str(all_config))
    
    for econfig in all_config:
        await register.exec_config(bot, econfig[:-5])