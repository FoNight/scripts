# coding:utf8

import MySQLdb
from xlwt import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#    __author__ = 'huazhanghui'
#    __date__ = '2018-05-24'
#    __Desc__ = 工具类

class Mysql():

    def getConn(self,host,user,passwd,dbname):
        conn=MySQLdb.connect(host, user, passwd, dbname, charset='utf8')
        return conn

    def getCursor(self,conn):
        cursor=self.getConn().cursor()
        return  cursor

    def seData(self,sql):
        self.sql = sql
        res = self.getConn().execute(sql)
        return res

    def inData(self,sql):
        self.sql = sql
        try:
            res = self.getConn().execute()
            print res
            self.getConn().commit()
        except:
            self.getConn().rollback()

    def upDate(self,sql,conn):
        self.sql = sql
        self.conn = self.getConn()


    # 给xls单元格加背景
    def changeColor(self,fields,results,outputpath):
        workbook = Workbook(encoding='utf-8')
        sheet_name='monitor'
        sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
        pattern=Pattern()
        fnt=Font()
        style=XFStyle()
        fnt.bold=True
        style.font=fnt
        pattern.pattern=Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour=23
        style.pattern = pattern
        for field in range(0, len(fields)):
            # pattern.pattern_fore_colour=22
            # style.pattern=pattern
            sheet.write(0, field, fields[field][0],style)

        row=1
        col=0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                pattern=Pattern()
                #borders=Borders()
                #borders.right=Borders.THIN
                #borders.top=Borders.THIN
                #borders.bottom=Borders.THIN
                #borders.left_colour=0x40
                #borders.right_colour=0x40
                #borders.top_colour=0x40
                #borders.bottom_colour=0x40
                style=XFStyle()
                #style.borders=borders
                pattern.pattern=Pattern.SOLID_PATTERN
                # 判断是否为字符串
                if (isinstance(results[row - 1][col], basestring)):
                    # 判断字符串内是否包含‘%’
                    if "%" in results[row - 1][col]:
                        a=float(results[row - 1][col].strip('%')) / 100

                        # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow
                        pattern.pattern_fore_colour=2
                        style.pattern=pattern
                        # 判断超过90%的显示红色
                        if (a >= 0.80):
                            #print a
                            sheet.write(row, col, u'%s' % results[row - 1][col], style)
                        # 80%~90% 的显示黄色
                        elif (0.6 < a < 0.8):
                            pattern.pattern_fore_colour=5
                            style.pattern=pattern
                            sheet.write(row, col, u'%s' % results[row - 1][col], style)
                        # 其余绿色显示
                        else:
                            pattern.pattern_fore_colour=3
                            style.pattern=pattern
                            sheet.write(row, col, u'%s' % results[row - 1][col], style)
                    else:
                        pattern.pattern_fore_colour = 22
                        style.pattern=pattern
                        sheet.write(row, col, u'%s' % results[row - 1][col])
                else:
                    pattern.pattern_fore_colour=22
                    style.pattern=pattern
                    sheet.write(row, col, u'%s' % results[row - 1][col])

        workbook.save(outputpath)
