"""
    接口关键字驱动封装
    将常用的请求方法进行函数封装，便于后续的可复用，易维护
"""

import requests
import json
import jsonpath

from config.log import get_log

log = get_log()


class Key:

    # 有些并不需要参数，默认为none, 其他的用 **kwargs传
    def do_get(self, url, params=None, headers=None, **kwargs):
        try:
            log.info('正在向{}发送get请求'.format(url))
            return requests.get(url=url, params=params, headers=headers, **kwargs)
        except Exception as e:
            log.error('get请求失败{}， url{}'.format(e, url))

    def do_post(self, url, params=None, headers=None, **kwargs):
        try:
            log.info('正在向{}发送post请求'.format(url))
            return requests.get(url=url, params=params, headers=headers, **kwargs)
        except Exception as e:
            log.error('post请求失败{}， url{}'.format(e, url))

    # 获取指定 key 文本信息，解析 json， 用于接口串联传递
    def get_text(self, response, key):
        if response is not None:
            try:
                if type(response) is str:
                    response = json.loads(response)   # 如果response返回的是字典，这里不需要, 这里是把 字符 转换为字典
                value = jsonpath.jsonpath(response, '$..{0}'.format(key))
                # 获取成功返回一个list, 失败 false
                if value:
                    if len(value) == 1:
                        return value[0]
                return value
            except Exception as e:
                return e
        else:
            return None

    # 对数据赋值的封装
    def assignment(self, kwargs):   # 字典数据内容
        for key, value in kwargs.items():
            if type(value) is dict:
                self.assignment(value)
            else:
                if value:
                    pass
                else:
                    kwargs[key] = getattr(self, key)   # 这里要求key 和value（self.key） key要相同
        return kwargs


"""
-
  path: api/createorder
  headers:
    token:
  data:
    openid:
    userid:
    productid: 8888
    cartid:
  result: success
三种情况，字典后面是字典 再迭代一次  字典后面有值 无需处理  字典后面无值  赋值
    url = 'http://127.0.0.1:5000/api/createorder'
    headers = {
        'token': self.token
    }
    data = {
        'openid': self.openid,
        'userid': self.userid,
        'productid': 8888,
        'cartid': self.cartid
    }
"""



