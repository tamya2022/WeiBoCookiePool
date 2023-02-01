"""
@file:api.py
@time:2019/11/8-16:29
"""
from flask import Flask, g
from CookiePool.db import *
from CookiePool.config import *


__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    初始化数据库
    :return:
    """
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))

    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机 Cookie
    :param website:
    :return:
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取 cookie 总数
    :param website:
    :return:
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8778)