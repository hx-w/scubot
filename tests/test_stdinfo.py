# -*- coding: utf-8 -*-
import json
import requests


def test_request():
    session = requests.session()
    cookies_str = ''
    cookies_dict = {}
    for line in cookies_str.split(';'):
        key, value = line.split('=', 1)
        cookies_dict[key] = value
    session.cookies = requests.utils.cookiejar_from_dict(cookies_dict, overwrite=True)

    url = 'http://ehall.scu.edu.cn/gsapp/sys/wdxj/xjqx/getXsInfo.do'
    headers = {
        # 'Referer': 'http://ehall.scu.edu.cn/gsapp/sys/wdxj/*default/index.do?t_s=1632811177273&amp_sec_version_=1&gid_=M3p4TFA3RWhSY3NpWUZPZG1NK1F4Wm1nKzFBaFpMR1Z2cGZIdk1XQWhyaGliQkRnNGE4NS82MVNocFhQL1lOUDZTZ2hPeUxxL0xQL2V5SHV5SGhzaEE9PQ&EMAP_LANG=zh&THEME=millennium'
    }
    resp = session.post(url=url)
    print(resp.status_code)
    resp_json = json.loads(resp.content.decode())
    print(resp_json)
    std_name = resp_json['xsInfoList'][0]['XM']
    std_id = resp_json['xsInfoList'][0]['XH']


    url = f'http://ehall.scu.edu.cn/gsapp/sys/zpglyy/showImageByds.do?XH={std_id}&&ZPLX=XJZP'
    resp = session.get(url=url)
    with open('std.jpg', 'wb') as ofile:
        ofile.write(resp.content)
    # print(resp.content.decode())


if __name__ == '__main__':
    test_request()
