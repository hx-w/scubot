# -*- coding: utf-8 -*-
import json
import requests
import redis

from . import scu_session


async def save_cookies(redis_inst: redis.Redis, redis_key: str, xk_token: str):
    redis_value = json.dumps({
        'XK_TOKEN': xk_token
    })
    redis_inst.set(redis_key, redis_value)


async def check_cookies_exists(redis_inst: redis.Redis, redis_key: str) -> bool:
    value = redis_inst.get(redis_key)
    if not value or len(value) == 0:
        return False
    try:
        json.loads(value)
        return True
    except Exception as ept:
        print('[ERROR] manual cookies str can not load to dict: %s' % ept)
        return False


async def update_cookies(session: requests.Session, redis_inst: redis.Redis, redis_key: str) -> requests.session:
    manual_cookies_str = redis_inst.get(redis_key)
    manual_cookies = json.loads(manual_cookies_str)
    cookiesJar = requests.utils.cookiejar_from_dict(
        manual_cookies, cookiejar=None, overwrite=True)
    session.cookies = cookiesJar
    session = await scu_session.session_login(session)
    return session
