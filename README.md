# Fecmall_test
一个在linux环境下部署开源平台Fecmall+Jenkins 的接口自动化项目，实现定时运行并发送测试报道

平台官网链接： https://www.fecmall.com/

linux环境为centos7 64位，采用docker的方式安装Fecmall, 
容器具体截图：
![image](https://user-images.githubusercontent.com/64000814/171036939-f7f3afb5-d0d1-4a08-80ba-ee9a28a7a3be.png)
python代码从上而下依次为 测试用例管理，配置，数据，关键字，日志及报告存放处

实现了注册，登录，查询用户，添加购物车，查询购物车，发送订单，查询订单等测试
![image](https://user-images.githubusercontent.com/64000814/171037849-909943da-cf9e-424a-859e-b5f515123881.png)

html报告如下

![image](https://user-images.githubusercontent.com/64000814/171038435-fe3e2c8a-9d70-4ceb-ae9e-4eaf343dd707.png)

在平台上登录也可以看到商品添加到购物车，订单提交等过程

![image](https://user-images.githubusercontent.com/64000814/171038186-050fee16-37cc-471d-ab91-30d533066111.png)
![image](https://user-images.githubusercontent.com/64000814/171038972-1c12e9ad-283b-483d-b12a-3a3c6f727ab0.png)
![image](https://user-images.githubusercontent.com/64000814/171039061-91478af2-19f8-4980-b96b-6f81e927dc1b.png)

Jenkins部分如下：
