# coding:utf8

import datetime
import time
import paramiko
import commands
import MySQLdb
from conStant import Constant

class test():

    def selData(self,host,user,pwd,db,sql,cpusql,sedisksql,disksql,sememsql,upmemsql,rrdfilepath,txtfilepath,upswapsql,seswapsql,sehomesql,homesql):
        conn=MySQLdb.connect(host, user, pwd, db, charset='utf8')
        cursor=conn.cursor()


        res = cursor.execute(sql)
        results = cursor.fetchall()
        fields = cursor.description
        row=1
        col=0

        for row in range(1, len(results) + 1):
            cpumonidata=''
            for col in range(0, len(fields)):
                if (col == 0):
                    ip = results[row - 1][col]
                else:
                    description = results[row - 1][col]
                    s = "".join(description)
                    rrdfilename =  s[11:]
                    txtfilename = s[11:-3]+'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
                    cpucmds="sed '1,2d;$d'" + " %s" % txtfile + "| sed \"s/-nan/0/g\" | awk '{  sum += $2 ; average = sum/NR} END { printf \"%.2f%\\n\", average }'"
		    res=commands.getoutput(rrd2txtcmd)
		    rest=commands.getoutput(cpucmds)
                    cpumonidata="".join(rest).split("\n")
	    cpuparm = cpumonidata+ip.split()
            cursor.execute(cpusql,cpuparm)
            conn.commit()


        sediskres=cursor.execute(sedisksql)
        diskres=cursor.fetchall()
        diskfields=cursor.description
        diskrow=1
        diskcol=0

        for diskrow in range(1, len(diskres) + 1):
            diskmonidata=''
            for diskcol in range(0, len(diskfields)):
                if (diskcol == 0):
                    ip=diskres[diskrow - 1][diskcol]
                    lip=ip.split()
                else:
                    description=diskres[diskrow - 1][diskcol]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
		    time.sleep(1)
                    diskcmds="sed '1,2d;$d'" + " %s" % txtfile + "| sed \"s/-nan/0/g\" | awk '{  sum += $2 ; average = sum/NR} END { printf \"%.2fG\\n\", " \
                             "average/1024/1024/1024;printf \"%.0fG\\n\",$3/1024/1024/1024+1 ; printf \"%.2f%\\n\",  average/$3*100 }'"
		    res=commands.getoutput(rrd2txtcmd)
                    rest=commands.getoutput(diskcmds)
                    diskmonidata="".join(rest).split("\n")
            diskparm=diskmonidata+lip
            cursor.execute(disksql,diskparm)
            conn.commit()

        seswapres=cursor.execute(seswapsql)
        swapres=cursor.fetchall()
        memfields=cursor.description
        swaprow=1
        swapcol=0
        for swaprow in range(1, len(swapres) + 1):
            for swapcol in range(0, len(memfields)):
                if (swapcol == 0):
                    lip=swapres[swaprow - 1][swapcol]
                else:
                    description=swapres[swaprow - 1][swapcol]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
                    swapcmds="sed '1,2d;$d'" + " %s" % txtfile + "| sed \"/-nan/d\"  | awk '{  sum += $2 ; average = sum/NR} END { printf \"%.2fG\\n\", average/1024/1024/1024 ;" \
                                                                 "printf \"%.0fG\\n\",$3/1024/1024/1024<20?$3/1024/1024/1024:$3/1024/1024/1024+1 }'"
		    res=commands.getoutput(rrd2txtcmd)
                    rest=commands.getoutput(swapcmds)
                    swapmonidata="".join(rest).split("\n")
            swapparm=swapmonidata + lip.split()
	    #print swapparm
            cursor.execute(upswapsql,swapparm)
            conn.commit()

        sehomeres=cursor.execute(sehomesql)
        homres=cursor.fetchall()
        homfields=cursor.description
        homrow=1
        homcol=0

        for homrow in range(1, len(homres) + 1):
            homemonidata=''
            for homcol in range(0, len(homfields)):
                if (homcol == 0):
                    ip=homres[homrow - 1][homcol]
                    hip=ip.split()
                else:
                    description=homres[homrow - 1][homcol]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
                    homecmds="sed '1,2d;$d'" + " %s" % txtfile + " | sed \"/-nan/d\" | awk '{  sum += $2 ; average = sum/NR} END { printf \"%.2fG\\n\", " \
                                                                 "average/1024/1024/1024;printf \"%.0fG\\n\",$3/1024/1024/1024+1 ; printf \"%.2f%\\n\",  average/$3*100 }'"

		    res=commands.getoutput(rrd2txtcmd)
                    rest=commands.getoutput(homecmds)
                    homemonidata="".join(rest).split("\n")
            homeparm=homemonidata + hip
            cursor.execute(homesql, homeparm)
            conn.commit()







        sememres=cursor.execute(sememsql)
        memres=cursor.fetchall()
        memfields=cursor.description
        memrow=1
        memcol=0
        percent=0
        for memrow in range(1, len(memres) + 1):
            diskmonidata=''
            for memcol in range(0, len(memfields)):
                if (memcol == 0):
                    ip=memres[memrow - 1][memcol]
                    lip=ip.split()
                else:
                    description=memres[memrow - 1][memcol]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
		    #print txtfile
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
                    memcmds="sed '1,2d;$d'" + " %s" % txtfile + " | sed \"/-nan/d\" | awk '{  sum += $2 ; average = sum/NR} END { printf \"%.2fG\\n\", average/1024/1024/1024 ;" \
                            "printf \"%.0fG\\n\",($3/1024/1024/1024<20 || $3/1024/1024/1024>100)?$3/1024/1024/1024:$3/1024/1024/1024+1 ; printf \"%.2f%\\n\", ($3!=0)?average/$3*100:0 }'"
                    #stdin, stdout, stderr=client.exec_command(rrd2txtcmd)
                    #stdin, stdout, stderr=client.exec_command(memcmds)
                    #memmonidata="".join(stdout.readlines())[:-1].split()
                    
		    res=commands.getoutput(rrd2txtcmd)
                    rest=commands.getoutput(memcmds)
		    memmonidata="".join(rest).split("\n")
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split(',')
            parm=memmonidata+nowTime+lip
            cursor.execute(upmemsql,parm)
            conn.commit()
        conn.close()
	print '更 新 完 成!'

