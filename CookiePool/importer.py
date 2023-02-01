"""
@file:importer.py
@time:2019/11/8-9:45
@info：账号录入器
"""
import time

from CookiePool.db import RedisClient


def set_account(site, type, account, sep=':'):
    conn = RedisClient(type, site)
    username, value = account.split(sep)

    num = 0
    while num < 5:
        result = conn.set(username, value)
        if result:
            print('{}--{} 录入成功! '.format(username, value))
            return
        num += 1
        time.sleep(1)

    print('录入失败, 请检查 redis内存是否已满, 尝试手动录入! ')


def scan(site):
    flag = input('录入账号请输入accounts, 录入Cookies请输入cookies，示例accounts\n')
    while True:
        account = input('请输入键值对(空格隔开), 输入 0 退出读入,示例lxb:123456\n')
        if account == '0':
            break

        set_account(site, flag, account)
