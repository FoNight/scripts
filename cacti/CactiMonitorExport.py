# coding:utf8
import os
import sys
from Util import Mysql
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = 'huazhanghui'
#    __date__ = '2018-05-24'
#    __Desc__ = 从数据库中导出数据到excel数据表中
import MySQLdb

class Xport():
    def export(self,host,user,password,dbname,outputpath):
        sql='select Hostname,Description,CPU_usp,Root_space_usd,Root_space_Total,Root_space_usp,Swap_usd,Swap_Total,Home_usd,Home_Total,Home_usp,Mem_us,Mem_Total,Mem_usp,buffers_cache,buffers_cache_p,UseFor,update_time from xport'
        conn = MySQLdb.connect(host,user,password,dbname,charset='utf8')
        cursor = conn.cursor()
        count = cursor.execute(sql)
        print '导出数据为：',count,' 条'
        # 重置游标位置
        cursor.scroll(0, mode='absolute')
        results=cursor.fetchall()

        # 获取MYSQL里面的数据字段名称
        fields=cursor.description

        #调用Util中 changeColor
        c = Mysql()
        c.changeColor(fields,results,outputpath)


        cursor.close()
        conn.close()


