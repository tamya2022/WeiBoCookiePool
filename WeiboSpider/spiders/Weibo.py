# -*- coding: utf-8 -*-
import json
from WeiboSpider.items import *


class ExampleSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    # 用户详情API
    user_url = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}"
    # 关注列表API
    follow_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}"
    # 微博列表API
    weibo_url_next = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}&since_id={since_id}"
    weibo_url_head = "https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}"

    start_users = ['2016802611']

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()

            field_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)

            yield user_item

            # 关注
            uid = user_info.get('id')
            yield scrapy.Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
                                 meta={'page': 1, 'uid': uid})

            yield scrapy.Request(self.weibo_url_head.format(uid=uid), callback=self.parse_weibos,
                                 meta={'uid': uid})

    def parse_follows(self, response):
        """
        解析用户关注
        :param response:
        :return:
        """
        result = json.loads(response.text)

        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) \
                and result.get('data').get('cards')[-1].get('card_group'):
            # 解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')

            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    # 生成解析关注用户信息的请求
                    yield scrapy.Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')

            # 存储关注者的ID
            user_relation_item = UserRelationItem()

            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for follow in
                       follows]

            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []

            yield user_relation_item
            # 下一页关注列表
            page = response.meta.get('page') + 1

            yield scrapy.Request(self.follow_url.format(uid=uid, page=page),
                                 callback=self.parse_follows, meta={'page': page, 'uid': uid})

    def parse_weibos(self, response):
        """
        解析微博列表
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')

            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                        'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic',
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item

            # 下一页微博
            uid = response.meta.get('uid')
            since_id = result.get('data').get('cardlistInfo').get('since_id')
            yield scrapy.Request(self.weibo_url_next.format(uid=uid, since_id=since_id), callback=self.parse_weibos,
                                 meta={'uid': uid})
