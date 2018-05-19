import logging
import logging.config
from os import path
import os

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')

server_log_path = "/data/logs/crawl/"


def init():
    # 文件夹不存在则创建
    if not path.exists(server_log_path):
        os.makedirs(server_log_path)
        logging.info(server_log_path + ' 创建成功')

    logging.config.fileConfig(log_file_path)


# 日志分离
class Logger:

    def info(self, msg, *args, **kwargs):
        logger = logging.getLogger("logger_info")
        logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logger = logging.getLogger("logger_error")
        logger.error(msg, *args, **kwargs)


log = Logger()
