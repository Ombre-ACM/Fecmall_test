# Fecmall_test
一个在linux环境下部署开源平台Fecmall+Jenkins 的接口自动化项目，实现jenkins按设置要求自动运行测试

平台官网链接： https://www.fecmall.com/

linux环境为centos7 64位，采用docker的方式安装Fecmall, 
容器具体截图：
![image](https://user-images.githubusercontent.com/64000814/172886819-24cddf4e-ef8a-4658-ab4c-2d075f4d5f22.png)


安装好后打开界面如下：
![image](https://user-images.githubusercontent.com/64000814/172886066-a84ea12f-0b87-4f74-90ec-32224a1b3f18.png)


python代码从上而下依次为 测试用例管理，配置，数据，关键字，日志及报告存放处

实现了注册，登录，查询用户，添加购物车，查询购物车，发送订单，查询订单等测试
![image](https://user-images.githubusercontent.com/64000814/171037849-909943da-cf9e-424a-859e-b5f515123881.png)

新的测试文件fecmall_testcase_ddt 通过ddt管理接口的测试用例，增加了接口的正向，逆向测试，包含请求头参数正确与否、请求参数必须参数，可选参数的
缺失与参数类型异常，重复提交请求等，最终增加到41个测试用例（加上请求头实际用例管理在50以上）

![image](https://user-images.githubusercontent.com/64000814/172884966-8a12f86a-f0bd-46bc-b1b7-149c786b21d5.png)


html报告如下

![image](https://user-images.githubusercontent.com/64000814/171038435-fe3e2c8a-9d70-4ceb-ae9e-4eaf343dd707.png)

在平台上登录也可以看到商品添加到购物车，订单提交等过程

![image](https://user-images.githubusercontent.com/64000814/171038186-050fee16-37cc-471d-ab91-30d533066111.png)
![image](https://user-images.githubusercontent.com/64000814/171038972-1c12e9ad-283b-483d-b12a-3a3c6f727ab0.png)
![image](https://user-images.githubusercontent.com/64000814/171039061-91478af2-19f8-4980-b96b-6f81e927dc1b.png)

Jenkins部分如下：

![image](https://user-images.githubusercontent.com/64000814/171139743-8677c4fa-39c2-49ff-b0af-8dd911ebe5b4.png)

![image](https://user-images.githubusercontent.com/64000814/171145727-8cc19228-012a-4017-a2fb-82f1bcd01ac7.png)


