import random
import unittest
import yaml
from request_key.keys import Key
from config.data_factory import get_register_data
from HTMLTestRunner import HTMLTestRunner
from ddt import ddt, file_data, data, unpack


@ddt
class FecMallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = Key()
        cls.url = 'http://appserver.fecmall.com'
        cls.token = None

    # 打开首页  无请求参数
    def test_001_index(self):
        url = self.url + '/cms/home/index'
        response = self.key.do_get(url=url)
        result = response.json()
        print('首页', result)

        expect_msg = "process success"
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 注册  使用 mimesis 构造的数据生成函数 随机构造 10 组正向注册数据
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

    # 注册错误，重复注册，构造缺参，参数异常等10组注册数据
    @file_data('../data/register_wrong.yaml')
    def test_003_register_wrong(self, **kwargs):
        url = self.url + '/customer/register/account'

        response = self.key.do_post(url=url, data=kwargs['data'])
        result = response.json()
        print(result)

        expect_msg = kwargs['message']
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 登录 包含账号错误，密码错误，缺账号，缺密码，以及 正确的账号密码
    @file_data('../data/user.yaml')
    def test_004_login(self, **kwargs):
        url = self.url + '/customer/login/account'

        response = self.key.do_post(url=url, data=kwargs['data'])
        result = response.json()
        print(result)
        print(response.headers)

        expect_msg = kwargs['message']
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

        # 错误的账号密码无法生成token，所以加个判断
        # 全局化 token，传递给下面的接口调用
        if result['message'] == 'process success':
            print(response.headers['Access-Token'])
            FecMallTest.token = response.headers['Access-Token']

    # 查询客户账号信息 参数只有一个token 设置正确， 错误/过期， 为空
    def test_005_customer_account(self):
        url = self.url + '/customer/account/index'
        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
            response = self.key.do_get(url=url, headers=headers)
            result = response.json()
            print(result)

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = "token is time out"

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户收货地址  参数只有一个token 设置正确， 错误/过期， 为空
    def test_006_customer_address(self):
        url = self.url + '/customer/address/index'
        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
            response = self.key.do_get(url=url, headers=headers)
            result = response.json()
            print(result)

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = "token is time out"

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 添加购物车  请求头参数headers 正确与异常与空 用例 随机 product_id  和 数量
    def test_007_product_add_cart(self):
        url = self.url + '/checkout/cart/add'
        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
            product_id = random.randint(1, 10)
            num = random.randint(1, 3)
            data = {'custom_option': {"my_color": "red", "my_size": "S", "my_size2": "S2", "my_size3": "S3"},
                    'product_id': str(product_id),
                    'qty': int(num)}
            response = self.key.do_post(url=url, data=data, headers=headers)
            result = response.json()
            print(result)

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = "token is time out"

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 添加购物车 请求参数异常 缺参 异常参数
    @file_data('../data/add_cart.yaml')
    def test_008_product_add_cart_wrong(self, **kwargs):
        url = self.url + '/checkout/cart/add'
        headers = {'Access-Token': self.token}

        response = self.key.do_post(url=url, data=kwargs['data'], headers=headers)
        result = response.json()
        print(result)

        expect_msg = kwargs['message']
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户购物车信息  只有请求头一个 token ，设置 正确，错误，为空
    def test_009_customer_cart(self):
        url = self.url + '/checkout/cart/index'

        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
            response = self.key.do_get(url=url, headers=headers)
            result = response.json()
            print(result)

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = "token is time out"

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 提交订单  这里先测试 请求头一个 token ，设置 正确，错误，为空
    def test_010_submit_order(self):
        url = self.url + '/checkout/onepage/submitorder'
        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
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

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = 'account not login or token timeout'

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')

    # 提交订单错误 用例测试 缺参，参数异常错误等
    @file_data('../data/order.yaml')
    def test_011_submit_order_wrong(self, **kwargs):
        url = self.url + '/checkout/onepage/submitorder'
        headers = {'Access-Token': self.token}

        response = self.key.do_post(url=url, data=kwargs['data'], headers=headers)
        result = response.json()
        print(result)

        expect_msg = kwargs['message']
        result_msg = result['message']

        self.assertEqual(expect_msg, result_msg, '断言失败')

    # 查询客户订单列表  测试 请求头一个 token ，设置 正确，错误，为空
    def test_012_customer_order(self):
        url = self.url + '/customer/order/index'
        headers_list = [{'Access-Token': self.token}, {'Access-Token': "AtPL0LXFPBV8CLoxxjpusFDEAGHsQ4F9"}, {'Access-Token': ""}]
        for headers in headers_list:
            response = self.key.do_get(url=url, headers=headers)
            result = response.json()
            print(result)

            if headers['Access-Token'] == self.token:
                expect_msg = "process success"
            else:
                expect_msg = 'token is time out'

            result_msg = result['message']
            self.assertEqual(expect_msg, result_msg, '断言失败')


if __name__ == '__main__':
    unittest.main()

