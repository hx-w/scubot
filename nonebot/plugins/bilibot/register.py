# -*- coding: utf-8 -*-

import os
import re
import time
import subprocess
import json
import aiocqhttp
import nonebot

from . import redis_utils

base_dir = '/data/bilibili-helper'
pattern_log = re.compile('20.*main - ')
log_host = 'https://bili.netlify.app/#/log?code='


async def get_all_config() -> list:
    list_dir = list(filter(lambda x: len(x) > 5 and x[-5:] == '.json', os.listdir(base_dir)))
    return list_dir


async def check_config_exist(qq_key: str) -> bool:
    return os.path.exists(f'{base_dir}/{qq_key}.json')


async def exec_config(bot: nonebot.NoneBot, qq_key: str):
    if not await check_config_exist(qq_key):
        await bot.send_private_msg(user_id=int(qq_key), message="未找到配置文件")
    __command = f'java -jar {base_dir}/BILIBILI-HELPER.jar {base_dir}/{qq_key}.json'
    exe = subprocess.Popen(__command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    await bot.send_private_msg(user_id=int(qq_key), message="即将开始执行B站签到脚本...请耐心等待")
    _tstart: float = time.time()
    ret, _ = exe.communicate()
    status = exe.wait()
    _tend: float = time.time()
    _cmin = int(_tend - _tstart) // 60
    _csec = int(_tend - _tstart) % 60
    message = "【执行成功】"
    if status != 0:
        message = "【执行失败】"
    message += f'耗时{_cmin}分{_csec}秒\n详细日志：'
    # save log
    retlines = ret.decode('utf-8')
    retlines = re.sub(pattern_log, '', retlines).encode('utf-8')
    code = f'{qq_key}-{int(time.time())}'
    await redis_utils.save_log(code, retlines)
    await bot.send_private_msg(user_id=int(qq_key), message=message + log_host + code)


async def save_config(qq_key: str, config_dict: dict) -> bool:
    global base_dir
    try:
        with open(f'{base_dir}/{qq_key}.json', 'w') as config_file:
            json.dump(config_dict, config_file)
        return True
    except:
        return False


async def handler_register(bot: nonebot.NoneBot, event: aiocqhttp.Event):
    # command parser
    if event.message[0]['type'] != 'text':
        return
    qq_key = str(event.user_id)
    raw_message: str = event.message[0]['data']['text'].strip().replace('\r\n', '')
    if '{' != raw_message[0]:
        return
    config_dict = {}
    try:
        config_dict = json.loads(raw_message)
        assert isinstance(config_dict['biliVerify']['biliCookies'], str)
    except:
        return
    if await check_config_exist(qq_key):
        await bot.send_private_msg(user_id=event.user_id, message="你已保存过配置文件，将替换旧的配置文件")
    if await save_config(qq_key, config_dict):
        await bot.send_private_msg(user_id=event.user_id, message="保存成功")
        await exec_config(bot, qq_key)
    else:
        await bot.send_private_msg(user_id=event.user_id, message="保存失败")
