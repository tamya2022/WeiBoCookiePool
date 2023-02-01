"""
@file:tester.py
@time:2019/11/8-9:51
@info: cookie检测器
"""
import json

import requests

from CookiePool.config import TEST_URL_MAP
from CookiePool.db import RedisClient


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()

        for username, cookies in cookies_groups.items():
            self.test(username.decode(), cookies.decode())


class WeiboValidTester(ValidTester):
    def __init__(self, website='Weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(f'正在测试Cookies 用户名:{username}')
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print(f'Cookies不合法:{username}')
            self.cookies_db.delete(username)
            print(f'删除Cookies:{username}')
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            print(f"test_url:{test_url}")

            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                content = json.loads(response.text)
                if content.get('data').get('cards')[0].get('desc') == '暂无可推荐的用户':
                    print(f'Cookies失效1:{username}')
                    self.cookies_db.delete(username)
                else:
                    print(f'Cookies有效:{username}')
            else:
                print(response.status_code, response.headers)
                print(f'Cookies失效2:{username}')
                self.cookies_db.delete(username)
                print(f'删除Cookies:{username}')
        except ConnectionError as e:
            print('发生异常', e.args)





