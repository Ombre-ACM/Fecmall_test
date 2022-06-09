import random
import unittest
from unittest import skip

from ddt import ddt, file_data, data, unpack

from request_key.keys import Key

from config.data_factory import get_register_data

@ddt
class FecMallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = Key()
        cls.url = 'http://appserver.fecmall.com'
        cls.token = None

    # 打开首页
    def test_001_index(self):
        url = self.url + '/cms/home/index'
        response = self.key.do_get(url=url)
        result = response.json()
        print('首页', result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 注册  使用 mimesis 构造的数据生成函数 随机构造 10 组注册数据
    def test_002_register(self):
        url = self.url + '/customer/register/account'
        data_list = get_register_data(iterations=10)

        for data in data_list:
            print(data)
            response = self.key.do_post(url=url, data=data)
            result = response.json()
            print(result)

            expect_msg = "process success"
            result_msg = result['message']

            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 登录  三组错误， 三组正确账号密码
    @file_data('../data/user.yaml')
    def test_003_login(self, **kwargs):
        url = self.url + '/customer/login/account'

        response = self.key.do_post(url=url, data=kwargs['data'])
        result = response.json()
        print(result)
        print(response.headers)

        # 错误的账号密码无法生成token，所以加个判断
        if kwargs['data']['password'] == '123456':
            expect_msg = "process success"
            print(response.headers['Access-Token'])
            FecMallTest.token = response.headers['Access-Token']
        else:
            expect_msg = "account login email or password is not correct"

        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户账号信息
    def test_004_customer_account(self):
        url = self.url + '/customer/account/index'
        headers = {'Access-Token': self.token}
        response = self.key.do_get(url=url, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户收货地址
    def test_005_customer_address(self):
        url = self.url + '/customer/address/index'
        headers = {'Access-Token': self.token}
        response = self.key.do_get(url=url, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 产品搜索
    @skip('接口文档错误')
    def test_006_product_search(self):
        url = self.url + '/catalogsearch/index/product'
        headers = {'Access-Token': self.token, 'fecshop_currency': 'CNY', 'fecshop-lang': 'zh'}
        data = {'q': "dress", 'filterAttrs': {"color": "red"}, 'price': "20-30", 'p': 2}

        response = self.key.do_get(url=url, headers=headers, data=data)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 产品详细信息
    def test_007_product_information(self):
        url = self.url + '/catalog/product/index'
        headers = {'Access-Token': self.token, 'fecshop_currency': 'CNY', 'fecshop-lang': 'zh'}
        data = {'product_id': "7"}
        response = self.key.do_get(url=url, data=data, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 添加收藏
    def test_008_product_add_favorite(self):
        url = self.url + '/catalog/product/favorite'
        headers = {'Access-Token': self.token}
        data = {'custom_option': {"my_color": "red", "my_size": "S", "my_size2": "S2", "my_size3": "S3"},
                'product_id': "7",
                'qty': 1}
        response = self.key.do_get(url=url, data=data, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 添加购物车  随机 product_id  和 数量, 添加3次
    def test_009_product_add_cart(self):
        for i in range(0, 3):

            product_id = random.randint(1, 10)
            num = random.randint(1, 5)

            url = self.url + '/checkout/cart/add'
            headers = {'Access-Token': self.token}
            data = {'custom_option': {"my_color": "red", "my_size": "S", "my_size2": "S2", "my_size3": "S3"},
                    'product_id': str(product_id),
                    'qty': int(num)}
            response = self.key.do_post(url=url, data=data, headers=headers)
            result = response.json()
            print(result)

            expect_msg = "process success"
            result_msg = result['message']

            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户购物车信息
    def test_010_customer_cart(self):
        url = self.url + '/checkout/cart/index'
        headers = {'Access-Token': self.token}
        response = self.key.do_get(url=url, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    def test_011_submit_order(self):
        url = self.url + '/checkout/onepage/submitorder'
        headers = {'Access-Token': self.token}
        data = {'address_id': '1',
                'billing': {'first_name': "yanjiang", 'last_name': "li", 'email': "1033817498@qq.com", 'telephone': "15757825661",
                            'street1': "杭州湾",
                            'street2': "",
                            'country': "CN",
                            'state': "ZJ",
                            'city': "宁波市",
                            'zip': "315336"},
                'customer_password': "",
                'confirm_password': "",
                'create_account': 0,
                'shipping_method': "fast_shipping",
                'payment_method': "paypal_standard"}
        response = self.key.do_post(url=url, data=data, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户订单列表
    def test_012_customer_order(self):
        url = self.url + '/customer/order/index'
        headers = {'Access-Token': self.token}
        response = self.key.do_get(url=url, headers=headers)
        result = response.json()
        print(result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')


if __name__ == '__main__':
    unittest.main()
