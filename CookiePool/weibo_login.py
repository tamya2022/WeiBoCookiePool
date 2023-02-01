"""
@file:weibo_login.py
@time:2019/11/8-15:29
"""
import random
import asyncio

from pyppeteer import launch


def input_time_random():
    return random.randint(20, 50)


class Weibo:
    def __init__(self, username, password):
        self.login_url = 'https://passport.weibo.cn/signin/login'
        if not username:
            raise "username is empty!!!"
        else:
            self.username = username
            self.password = password

    async def start(self):
        """
        输入账号密码并点击登录....
        :return:
        """
        browser = await launch({'headless': False})
        context = await browser.createIncogniteBrowserContext()
        page = await context.newPage()
        await page.goto(self.login_url)

        await page.waitFor(2000)
        await page.hover('#loginName')
        await page.mouse.down()
        await page.mouse.up()

        await page.type('input#loginName', self.username, {'delay': input_time_random()})
        await page.type('input#loginPassword', self.password, {'delay': input_time_random()})
        await asyncio.sleep(1)

        await page.click('a#loginAction')

        await page.waitFor(6000)
        content = await page.content()
        # 判断是否登录成功：
        elements = await page.xpath('//div[@id="app"]')
        if not elements:
            if "点击按钮进行验证" in content:
                click_btn = page.xpath("//span[@class='geetest_radar_tip_content']")[0]
                click_btn.click()
                return await self.get_cookie(page)
            else:
                print("登录失败...")
        else:
            cookie = await self.get_cookie(page)
            await browser.close()
            return cookie

    async def get_cookie(self, page):
        """
        获取 cookies....
        :return:
        """
        cookie_dict = dict()
        cookies_dict_in_list = await page.cookies()
        for cookie in cookies_dict_in_list:
            cookie_dict[cookie['name']] = cookie['value']
        # cookies = ''
        # for cookie in cookies_list:
        #     str_cookie = '{0}={1};'
        #     str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        #     cookies += str_cookie
        cookie_dict_status = {"status": 1, "content": cookie_dict}
        return cookie_dict_status


if __name__ == '__main__':
    username = input("输入账号:")
    password = input("输入密码:")
    # 多账户读取时可用如下格式的文本
    # 账号1|密码1
    # 账号2|密码2
    # 账号3|密码3
    wb = Weibo(username, password)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(wb.start())
    loop.run_until_complete(task)
    print(task.result())
