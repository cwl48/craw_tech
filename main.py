# -*- coding: utf-8 -*-
from conf import logger
from crawler import juejin, cnblog, kf_toutiao, tuiku, importnew, imooc, bole, jianshu, csdn
from gw import controller

if __name__ == '__main__':
    # log配置
    logger.init()
    # 启动
    controller.init()
