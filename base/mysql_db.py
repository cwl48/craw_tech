# -*- coding: utf-8 -*-
import pymysql

from conf.logger import log
from conf.conf import db
from DBUtils.PooledDB import PooledDB, SharedDBConnection

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示没有限制
    mincached=5,  # 初始化时，连接池至少创建的空闲的连接，0表示不创建
    maxcached=10,  # 连接池空闲的最多连接数，0和None表示没有限制
    maxshared=5,
    # 连接池中最多共享的连接数量，0和None表示全部共享，ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
    blocking=True,  # 链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,  # ping Mysql 服务端，检查服务是否可用
    host=db["host"],
    port=db['port'],
    user=db['user'],
    password=db['passwd'],
    database=db['db'],
    charset='utf8'
)


class _MySQL(object):
    conn = None

    def __init__(self):
        self.conn = POOL.connection()

    def get_cursor(self, param=None):
        return self.conn.cursor(param)

    def query_one(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            result = cursor.fetchone()
        except Exception as e:
            log.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result

    def query(self, sql):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()
        except Exception as e:
            log.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result

    def execute(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception as e:
            log.error("mysql execute error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_row

    def executemany(self, sql, params=None):
        cursor = self.get_cursor()
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            log.error("mysql executemany error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_rows

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        self.close()


mysql = _MySQL()

