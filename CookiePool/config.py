# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 21:32
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : config.py
# @Software: PyCharm

# Redis 数据库链接
REDIS_URL = 'redis://@localhost:6379/1'

# 代理池地址
PROXY_URL = 'http://localhost:5000/random/'

# 站点集合
SITE_LIST = ['Amazon', 'Jingdong', 'Dangdang']

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'Weibo': 'WeiboCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'Weibo': 'WeiboValidTester'
}

TEST_URL_MAP = {
    # 'Weibo': 'https://m.weibo.cn/profile/6207269327'
    'Weibo': 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followersrecomm_-_2016802611&luicode=10000011&lfid=1005052016802611&featurecode=10000326'
}

# 生成器循环周期
GENERATOR_CYCLE = 60 * 30

# 检测器循环周期
TESTER_CYCLE = 60 * 30

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 8888

# 账号注册器开关
ACCOUNT_GENERATOR_PROCESS = True

# Cookies 生成器开关，模拟登录添加 Cookies
COOKIES_GENERATOR_PROCESS = True

# 检测器开关，循环检测数据库中 Cookies 是否可用，不可用删除
VALID_PROCESS = False

# API接口服务: API 接口放在线上服务器跑, 注册登录检测放在线下服务器跑
API_PROCESS = False
