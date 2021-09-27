# -*- coding: utf-8 -*-
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}


async def session_login(session: requests.Session) -> requests.Session:
    url = 'http://ehall.scu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadKbxx.do'
    resp = session.get(url=url, headers=headers)
    if resp.status_code != 200:
        print('[ERROR] response in <session_login> is %d' % resp.status_code)
    return session
