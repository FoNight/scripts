# coding:utf8


import MySQLdb
from conStant import Constant

class ExportDb():
    def insert(self,host,user,pwd,db,sesql,insql):
        conn = MySQLdb.connect(host,user,pwd,db,charset='utf8')
        cursor = conn.cursor()
        result = cursor.execute(sesql)
        print 'host_info 数据条数：',result
        cursor.scroll(0, mode='absolute')
        results=cursor.fetchall()
        row=1
        for row in range(1, len(results)+1):
            try:
                res = cursor.execute(insql,results[row-1])
                conn.commit()
            except:
                conn.rollback()

        conn.close()


