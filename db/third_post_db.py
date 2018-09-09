# -*- coding: utf-8 -*-
from base import mysql_db
from conf.logger import log


# 第三方文章DB
class _ThirdPostDB:
    table = "tb_third_post"

    # 根据objectId,thirdId查询文章信息
    def find_by_pt_id(self, post_id, third_id):
        db = mysql_db.mysql
        sql = "select title from tb_third_post where object_id=%s and third_type=%s"
        try:
            data = db.query_one(sql, (post_id, third_id))
            return data
        except Exception as e:
            log.info("执行Mysql: %s 时出错：%s" % (sql, e))

    # 批量插入
    def batch_insert(self, list):

        db = mysql_db.mysql
        sql = "insert into tb_third_post (third_type,third_name," \
              "object_id,title,tags,author,content,like_num,comment_num,redirect_url,creatime,can_analysis,created_at) values(%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,now())"
        try:
            db.executemany(sql, list)
        except Exception as e:
            log.info("执行Mysql: %s 时出错：%s" % (sql, e))


third_post_db = _ThirdPostDB()
