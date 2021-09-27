import json
import requests

def is_json(content: str) -> bool:
    try:
        json.loads(content)
        return True
    except:
        return False

def test_request():
    # url = 'http://ehall.scu.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadKbxx.do'
    url = 'http://ehall.scu.edu.cn/jsonp/getTaskMessageCount'
    session = requests.session()

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    }

    manual_cookies = {
        'AUTHTGC': 'fm3gEuS4l4qio8Q9rcsZ0K8qcu85h/fNK8lVFpDirm+UCsQAPlfA0w==',
        'MOD_AMP_AUTH': 'MOD_AMP_fd1f22a3-6dd7-473e-a0d5-bada4c7cc65d',
        
    }

    cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)

    session.cookies = cookiesJar
    print(type(cookiesJar))
    resp = session.get(url, headers=header)

    assert resp.status_code == 200
    assert is_json(resp.content.decode()), resp.content.decode()


if __name__ == '__main__':
    test_request()