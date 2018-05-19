from conf import logger
from base import scheduled
from crawler import juejin

if __name__ == '__main__':
    # log配置
    logger.init()

    # 定时任务启动
    scheduled.start()
    juejin.JueJin().start()
