import logging


def get_log():
    # 创建一个日志器
    logger = logging.getLogger()

    # 设置级别 debug info 不知输出到哪里
    logger.setLevel(logging.INFO)
    # 创建控制台处理器
    sh = logging.StreamHandler()
    # 添加到控制台
    logger.addHandler(sh)
    # 设置格式 创建格式器
    formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s %(message)s')
    # 控制台获取格式
    sh.setFormatter(formatter)

    # 保存在文件中
    fh = logging.FileHandler('../result/log_result.log', encoding='utf-8')
    logger.addHandler(fh)
    fh.setFormatter(formatter)

    return logger
