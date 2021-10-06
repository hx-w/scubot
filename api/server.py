import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import redis


redis_inst: redis.Redis = redis.Redis(
    host='redis', port=6379, decode_responses=True)

config_dir = '/data/certfiles'

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/query_log")
async def server_info(code: str):
    ret = redis_inst.get(code)
    if ret:
        return ret
    return 'Not Found'

if __name__ == '__main__':
    keyfile_path = os.path.join(config_dir, 'private.pem')
    certfile_path = os.path.join(config_dir, 'fullchain.crt')
    if os.path.exists(keyfile_path) and os.path.exists(certfile_path):
        uvicorn.run(
            api,
            host="0.0.0.0",
            port=8080,
            ssl_keyfile=keyfile_path,
            ssl_certfile=certfile_path
        )
    else:
        uvicorn.run(api, host="0.0.0.0", port=8080)
