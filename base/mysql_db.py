# -*- coding: utf-8 -*-
import pymysql

from conf.logger import log
from conf.conf import db


class _MySQL(object):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset=charset)

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


host = db["host"]
port = db['port']
user = db['user']
passwd = db['passwd']
db = db['db']

mysql = _MySQL(host, port, user, passwd, db)
