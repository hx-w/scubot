# -*- coding: utf-8 -*-

import aiocqhttp
import nonebot

from . import register

bot: nonebot.NoneBot = nonebot.get_bot()


@bot.on_message('private')
async def handler_on_message(event: aiocqhttp.Event):
    await register.handler_register(bot, event)


# @bot.asgi.route('/query_log', methods=['GET'])
# @route_cors(allow_origin=['*'])
# async def query_code():
#     code = request.args.get('code', '')
#     ret_log = await redis_utils.get_log(code)
#     if ret_log:
#         return ret_log
#     return 'Not Found'