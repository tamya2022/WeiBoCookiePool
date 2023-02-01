"""
@file:runImporter.py
@time:2019/11/8-10:28
"""
from CookiePool.importer import scan
from CookiePool.tester import WeiboValidTester

if __name__ == '__main__':
    dtype = input("a:录入 b：测试 -- ")
    if dtype == 'a':
        hashName = "Weibo"
        scan(hashName)
    else:
        print("开始测试...")
        WeiboValidTester().run()
