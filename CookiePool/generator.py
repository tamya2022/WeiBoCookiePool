"""
@file:generator.py.py
@time:2019/11/8-9:10
"""
import asyncio
import json

from CookiePool.weibo_login import Weibo
from CookiePool.db import RedisClient


class CookiesGenerator:
    def __init__(self, website, single_cycle_limit):
        """
        父类, 初始化一些对象
        :param website: 名称
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.single_cycle_limit = single_cycle_limit

    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def run(self):
        """
        得到所有账户, 然后按序模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        if not accounts_usernames:
            print(f"accounts is empty!!")
            raise

        num = 0
        for username in accounts_usernames:

            if num >= self.single_cycle_limit:
                print('已达单轮登录上限, 停止登录! ')
                return

            if username not in cookies_usernames:
                username = username.decode()
                password = self.accounts_db.get(username).decode()

                print(f'{self.website}正在生成Cookies,{username}:{password}')

                result = self.new_cookies(username, password)
                if result.get("status") == 1:
                    cookies = result.get("content")
                    if cookies is not None:
                        print(f'成功获取到Cookies:{cookies}')
                        if self.cookies_db.set(username, json.dumps(cookies)):
                            print(f'成功保存Cookies...')
                            num += 1
                    else:
                        print(f"无Cookie，可能账号输错，不进行保存...")

        else:
            print(f'所有账号都已经成功处理...')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self, website='Weibo'):
        self.site = website
        # 限制单轮登录
        self.single_cycle_limit = 2
        CookiesGenerator.__init__(self, self.site, self.single_cycle_limit)

    def new_cookies(self, username, password):
        """
        生成 cookies
        :param username:
        :param password:
        :return:
        """
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(Weibo(username, password).start())

        return result


if __name__ == '__main__':
    wbcookie = WeiboCookiesGenerator()
    wbcookie.run()
