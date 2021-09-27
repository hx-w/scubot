# -*- coding: utf-8 -*-
import typing
import json
import redis

redis_inst: redis.Redis = redis.Redis(
    host='redis', port=6379, decode_responses=True)


async def save_cookies(redis_key: str, redis_value: dict):
    redis_inst.set(str(redis_key), json.dumps(redis_value))


async def get_cookies(qq_key: str) -> typing.Tuple[bool, dict]:
    manual_cookies_str = redis_inst.get(qq_key)
    try:
        manual_cookies = json.loads(manual_cookies_str)
        return True, manual_cookies
    except Exception as ept:
        print('[ERROR] manual cookies str can not load to dict: %s' % ept)
        return False, {}


async def get_all_keys() -> list:
    return redis_inst.keys()