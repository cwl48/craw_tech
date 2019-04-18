# -*- coding: utf-8 -*-
from flask_apscheduler import APScheduler
from crawler import juejin, kf_toutiao, tuiku, cnblog, importnew, imooc, bole, segment,infoq,jianshu
from util import myos


class Config:
    JOBS = [
        {
            'id': 'juejin',              # 掘金文章爬取任务
            'func': 'crawler.juejin:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 1
        },
        {
            'id': 'kf_toutiao',              # 开发者头条爬取任务
            'func': 'crawler.kf_toutiao:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,1,3,8,9,10,11,13,18,19,20,23',                # 每天16：26分执行
            'minute': 35
        },
        {
            'id': 'tuiku',              # 推酷爬取任务
            'func': 'crawler.tuiku:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 10
        },
        {
            'id': 'cnblog',              # 博客园爬取任务
            'func': 'crawler.cnblog:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 20
        },
        {
            'id': 'importnew',              # importNew 爬取任务
            'func': 'crawler.importnew:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 30
        },
        {
            'id': 'imooc',              # imooc 爬取任务
            'func': 'crawler.imooc:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 40
        },
        {
            'id': 'bole',              # 伯乐在线 爬取任务
            'func': 'crawler.bole:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,5,8,10,11,13,16,18,19,20,22,23',                # 每天16：26分执行
            'minute': 50
        },
        {
            'id': 'segment',              # segment 爬取任务
            'func': 'crawler.segment:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,8,11,18,22',                # 每天16：26分执行
            'minute': 59
        },
        {
            'id': 'infoq',              # segment 爬取任务
            'func': 'crawler.infoq:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,8,9,11,15,18,20,22',                # 每天16：26分执行
            'minute': 23
        },
        {
            'id': 'jianshu',              # segment 爬取任务
            'func': 'crawler.jianshu:start',  # 定时执行的 模块：函数
            'trigger': 'cron',         # 定时执行，其他可选参数data,interval
            'hour': '0,8,9,11,15,18,20,22',                # 每天16：26分执行
            'minute': 49
        }
    ]


def do_start(app):
    sched = APScheduler()
    app.config.from_object(Config())
    sched.init_app(app)
    sched.start()


def start(app):
    # linux下开起定时任务  其他就直接全部执行
    if myos.is_linux():
        do_start(app)
    else:
        # juejin.JueJin().start()

        # tuiku.TuiKu().start()
        # kf_toutiao.KaiFaTouTiao().start()
        # importnew.ImportNew().start()
        # cnblog.CnBlog().start()
        # imooc.Imooc().start()
        # bole.Bole().start()
        # jianshu.JianShu().start()
        # csdn.Csdn().start()
        # segment.Segment().start()
        # infoq.InfoQ().start()
        print("pass")
