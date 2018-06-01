from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import juejin, kf_toutiao, tuiku, cnblog, importnew


def start():
    sched = BlockingScheduler()

    # 掘金文章爬取任务
    sched.add_job(juejin.JueJin().start, 'cron', hour='6,12,18,22,1', minute=1)
    # 开发者头条爬取任务
    sched.add_job(kf_toutiao.KaiFaTouTiao().start, 'cron', hour='6,10,11,18,23', minute=10)
    # 推酷爬取任务
    sched.add_job(tuiku.TuiKu().start, 'cron', hour='5,9,11,20,23', minute=3)
    # 博客园爬取任务
    sched.add_job(cnblog.CnBlog().start, 'cron', hour='5,9,11,20,23', minute=20)
    # importNew 爬取任务
    sched.add_job(importnew.ImportNew().start, 'cron', hour='5,9,11,20,23', minute=40)

    sched.start()
