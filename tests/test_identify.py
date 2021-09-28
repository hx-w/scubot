# -*- coding: utf-8 -*-
import requests


def test_request():
    session = requests.session()
    cookies_str = ''
    cookies_dict = {}
    for line in cookies_str.split(';'):
        key, value = line.split('=', 1)
        cookies_dict[key] = value
    session.cookies = requests.utils.cookiejar_from_dict(cookies_dict, overwrite=True)

    url = 'http://ehall.scu.edu.cn/gsapp/sys/wdcjapp/modules/wdcj/xscjcx.do'
    resp = session.post(url=url)
    print(resp.status_code)
    print(resp.content.decode())

    url = 'http://ehall.scu.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/xsjxrwcx.do'
    post_data = {
        'XNXQDM': 20211,
        'pageNumber': 1,
        'pageSize': 20
    }
    resp = session.post(url, data=post_data)
    print(resp.status_code)


if __name__ == '__main__':
    test_request()
