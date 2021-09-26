from nonebot import get_bot, on_notice, NoticeSession, on_websocket_connect

bot = get_bot()

@on_notice('notify')
async def poke(session: NoticeSession):
    print('???')