# -*- coding: utf-8 -*-
import redis

redis_inst: redis.Redis = redis.Redis(
    host='redis', port=6379, decode_responses=True)


async def save_log(code: str, log: bytes):
    redis_inst.set(code, log)


async def get_log(code: str) -> str:
    return redis_inst.get(code)
