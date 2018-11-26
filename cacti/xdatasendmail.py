# coding:utf8
import commands
import time
from conStant import Constant
from queryRrdData import ExportDb
from insertMoniData import test
from CactiMonitorExport import Xport
from wInserData import WinInsert
from upCached import Upcached

class XdataSendMail():
    def sendmail(self,mailuser):
        filecmd="ls -t /home/reports | head -n 1"
        Cactifile=commands.getoutput(filecmd)
        cmd="cat /home/scripts/moni_msg | mailx -s '运维服务部周监控信息' -a /home/reports/%s"%Cactifile\
            +"%s "%mailuser
        res=commands.getoutput(cmd)
        print '邮件发送成功！'

    def xs(self,host,user,pwd,db,sesql,insql):
        inhostinfo = ExportDb()
        inhostinfo.insert(host,user,pwd,db,sesql,insql)

    def seD(self,host,user,pwd,db,sql,cpusql,sedisksql,disksql,sememsql,upmemsql,rrdfilepath,txtfilepath,upswapsql,seswapsql,sehomesql,homesql):
        inmonidata = test()
        inmonidata.selData(host,user,pwd,db,sql,cpusql,sedisksql,disksql,sememsql,upmemsql,rrdfilepath,txtfilepath,upswapsql,seswapsql,sehomesql,homesql)

    def xData(self,host,user,pwd,dbname,outputpath):
        xd=Xport()
        xd.export(host,user,pwd,dbname,outputpath)

    def xWinData(self,host,user,pwd,db,wincpusql,rrdfilepath,txtfilepath,upwincpu,windisksql,upwindisk):
        xw = WinInsert()
        xw.createRrdfile(host,user,pwd,db,wincpusql,rrdfilepath,txtfilepath,upwincpu,windisksql,upwindisk)

    def upCached(self,host,user,pwd,db,cachedsql,rrdfilepath,txtfilepath,buffersql,memTotal,upCachp,upCached):
        uc = Upcached()
        uc.upCachedData(host,user,pwd,db,cachedsql,rrdfilepath,txtfilepath,buffersql,memTotal,upCachp,upCached)

if __name__ == '__main__':
    x = XdataSendMail()
    c=Constant()
    sesql=c.seHostDes()
    insql=c.inHostDes()
    host=c.getHost()
    user=c.getDbUser()
    pwd=c.getDbPwd()
    db=c.getDbName()
    x.xs(host,user,pwd,db,sesql,insql)


    rrdfilepath=c.getRrdPath()
    txtfilepath=c.getTxtPath()
    sql=c.getSeCpuSql()
    cpusql=c.upCpuSql()
    sedisksql=c.getSeDiskSql()
    disksql=c.upDiskSql()
    upswapsql=c.upSwapSql()
    sememsql=c.getSeMemSql()
    upmemsql=c.upMemSql()
    seswapsql=c.getSeSwapSql()
    sehomesql=c.getHomeSql()
    homesql=c.upHomesql()
    x.seD(host,user,pwd,db,sql,cpusql,sedisksql,disksql,sememsql,upmemsql,rrdfilepath,txtfilepath,upswapsql,seswapsql,sehomesql,homesql)
    time.sleep(1)

    wincpusql=c.winCpusql()
    windisksql=c.winDisk()
    x.xWinData(host,user,pwd,db,wincpusql,rrdfilepath,txtfilepath,cpusql,windisksql,disksql)


    cachedsql=c.getCached()
    buffersql=c.getBuffer()
    memTotal=c.getMemtotal()
    upCachp=c.upCachp()
    upCached=c.upCached()
    x.upCached(host,user,pwd,db,cachedsql,rrdfilepath,txtfilepath,buffersql,memTotal,upCachp,upCached)


    
    filename=c.getXname()
    filepath=c.reportpath()
    out_path=filepath+filename
    x.xData(host,user,pwd,db,out_path)

    mailusers=c.mailuserlist()
    x.sendmail(mailusers)

