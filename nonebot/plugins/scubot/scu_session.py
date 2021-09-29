# -*- coding: utf-8 -*-
import json
import requests

from . import redis_utils

session_dict = {}  # str: Session

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}


async def add_session_dict(qq_key: str):
    global session_dict
    session_dict[qq_key] = requests.session()


async def session_login(qq_key: str) -> bool:
    global session_dict
    try:
        cookiesJar = requests.utils.cookiejar_from_dict(
            (await redis_utils.get_cookies(qq_key))[1], cookiejar=None, overwrite=True)
        session_dict[qq_key].cookies = cookiesJar
        url = 'http://ehall.scu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadKbxx.do'
        resp = session_dict[qq_key].get(url=url, headers=headers)
        if resp.status_code != 200:
            print('[ERROR] response in <session_login> is %d' %
                  resp.status_code)
            return False
        redis_utils.save_cookies(
            qq_key, session_dict[qq_key].cookies.get_dict())
        print(
            f'[INFO] 已更新session cookies => {session_dict[qq_key].cookies.get_dict()}')
        return True
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return False


async def get_student_info(qq_key: str) -> dict:
    global session_dict
    try:
        cookiesJar = requests.utils.cookiejar_from_dict(
            (await redis_utils.get_cookies(qq_key))[1], overwrite=True)
        session_dict[qq_key].cookies = cookiesJar
        url = 'http://ehall.scu.edu.cn/gsapp/sys/wdxj/xjqx/getxsinfo.do'
        resp = session_dict[qq_key].post(url=url, headers=headers)
        if resp.status_code != 200:
            print('[ERROR] response in <get_student_info> is %d' %
                  resp.status_code)
            return {}
        redis_utils.save_cookies(
            qq_key, session_dict[qq_key].cookies.get_dict())
        print(
            f'[INFO] 已更新session cookies => {session_dict[qq_key].cookies.get_dict()}')
        return json.loads(resp.content.decode())
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return {}


async def get_student_picture(qq_key: str, std_id: str) -> bool:
    global session_dict
    try:
        cookiesJar = requests.utils.cookiejar_from_dict(
            (await redis_utils.get_cookies(qq_key))[1], cookiejar=None, overwrite=True)
        session_dict[qq_key].cookies = cookiesJar

        url = f'http://ehall.scu.edu.cn/gsapp/sys/zpglyy/showImageByds.do?XH={std_id}&&ZPLX=XJZP'
        resp = session_dict[qq_key].get(url=url, headers=headers)
        if resp.status_code != 200:
            print('[ERROR] response in <get_student_picture> is %d' %
                  resp.status_code)
            return False
        redis_utils.save_cookies(
            qq_key, session_dict[qq_key].cookies.get_dict())
        print(
            f'[INFO] 已更新session cookies => {session_dict[qq_key].cookies.get_dict()}')
        with open(f'{std_id}.jpg', 'wb') as ofile:
            ofile.write(resp.content)
        return True
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return False


async def get_grade_list(qq_key: str) -> dict:
    global session_dict
    try:
        cookiesJar = requests.utils.cookiejar_from_dict(
            (await redis_utils.get_cookies(qq_key))[1], cookiejar=None, overwrite=True)
        session_dict[qq_key].cookies = cookiesJar
        url = 'http://ehall.scu.edu.cn/gsapp/sys/wdcjapp/modules/wdcj/xscjcx.do'
        resp = session_dict[qq_key].post(url=url, headers=headers)
        if resp.status_code != 200:
            print('[ERROR] response in <get_grade_list> is %d' %
                  resp.status_code)
            return {}
        redis_utils.save_cookies(
            qq_key, session_dict[qq_key].cookies.get_dict())
        print(
            f'[INFO] 已更新session cookies => {session_dict[qq_key].cookies.get_dict()}')
        return json.loads(resp.content.decode())
    except Exception as ept:
        print(f'[ERROR] {ept}')
        return {}
