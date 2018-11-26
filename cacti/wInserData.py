# coding:utf8

import commands
import MySQLdb


class WinInsert():
    def createRrdfile(self,host,user,pwd,db,wincpusql,rrdfilepath,txtfilepath,upwincpu,windisksql,upwindisk):
        conn=MySQLdb.connect(host, user, pwd, db, charset='utf8')
        cursor=conn.cursor()

        res=cursor.execute(wincpusql)
        results=cursor.fetchall()
        fields=cursor.description
        row=1
        col=0

        for row in range(1, len(results) + 1):
            cpumonidata=''
            for col in range(0, len(fields)):
                if (col == 0):
                    ip=results[row - 1][col]
                else:
                    description=results[row - 1][col]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    #print  rrdfile,txtfile
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day AVERAGE > %s' % txtfile
                    wcpucmds="sed -e '/-nan/d'" + " %s" % txtfile + " | sed '1,2d;$d' | awk '{sum+=$8 ;average=sum/NR} END {printf \"%.2f%\\n\", average}'"
                    res=commands.getoutput(rrd2txtcmd)
                    rest=commands.getoutput(wcpucmds)
                    cpumonidata="".join(rest).split("\n")
            cpuparm=cpumonidata + ip.split()
            #print  ip.split()
            cursor.execute(upwincpu, cpuparm)
            conn.commit()


        wres=cursor.execute(windisksql)
        wresults=cursor.fetchall()
        wfields=cursor.description
        wrow=1
        wcol=0

        for wrow in range(1, len(wresults) + 1):
            wdiskmonidata=''
            for wcol in range(0, len(wfields)):
                if (wcol == 0):
                    ip=wresults[wrow - 1][wcol]
                else:
                    description=wresults[wrow - 1][wcol]
                    s="".join(description)
                    rrdfilename=s[11:]
                    txtfilename=s[11:-3] + 'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    print  rrdfile,txtfile
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day MAX > %s' % txtfile
                    wdiskcmds="sed '1,2d;$d'" + " %s" % txtfile + " | sed '/-nan/d' |awk '{  sum += $2 ; " \
                              "average = sum/NR} END { printf  \"%.2fG\\n\", average/1024/1024/1024;printf  \"%.0fG\\n\",$3/1024/1024/1024 ; printf \"%.2f%\\n\",  average/$3*100 }'"
                    wrrdres=commands.getoutput(rrd2txtcmd)
                    wcmdres=commands.getoutput(wdiskcmds)
                    wdiskmonidata="".join(wcmdres).split("\n")
            wdiskparm=wdiskmonidata + ip.split()
            print  wdiskparm
            cursor.execute(upwindisk, wdiskparm)
            conn.commit()
	print 'windows update succ ! '
# if __name__ == "__main__":
#     c = Constant()
#     host = c.getHost()
#     user = c.getDbUser()
#     pwd = c.getDbPwd()
#     db = c.getDbName()
#     wincpusql = c.winCpusql()
#     windisksql = c.winDisk()
#     upwincpu = c.upCpuSql()
#     upwindisk = c.upDiskSql()
#     rrdfilepath = c.getRrdPath()
#     txtfilepath = c.getTxtPath()
#     w = WinInsert()
#     w.createRrdfile(host,user,pwd,db,wincpusql,rrdfilepath,txtfilepath,upwincpu,windisksql,upwindisk)
