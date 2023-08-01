import logging

from logging import handlers


class Mylogger(object):
    def __init__(self, logfile):
        # 1.指明日志记录到哪个文件 "F:/xxx/xx" + "info.config"
        # 2.配置日志操作器
        handler = handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024 * 8, backupCount=5, encoding='utf-8')
        # 3.设置日志格式
        fmt = "%(levelname)s-%(asctime)s-%(module)s-%(lineno)d-%(message)s"
        # 4. 配置格式实例
        formatter = logging.Formatter(fmt)
        # 5.操作器加载格式实例
        handler.setFormatter(formatter)
        # 6.创建logger实例
        self.logger = logging.getLogger()
        # 7.给实例增加日志操作器
        self.logger.addHandler(handler)
        # 8.给实例增加日志输出登记
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self.logger
