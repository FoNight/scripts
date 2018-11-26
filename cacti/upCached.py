# coding:utf8

import MySQLdb
import commands

class Upcached():

    def upCachedData(self,host,user,pwd,db,cachedsql,rrdfilepath,txtfilepath,buffersql,memTotal,upCachp,upCached):
        conn=MySQLdb.connect(host, user, pwd, db, charset='utf8')
        cursor=conn.cursor()


        res = cursor.execute(cachedsql)
        results = cursor.fetchall()
        fields = cursor.description
        row=1
        col=0
        num = 0
        for row in range(1, len(results) + 1):
            cachmonidata=''.split()

            for col in range(0, len(fields)):
                if (col == 0):
                    ip = results[row - 1][col]
                    num+=1
                else:
                    description = results[row - 1][col]
                    s = "".join(description)
                    rrdfilename =  s[11:]
                    txtfilename = s[11:-3]+'txt'
                    rrdfile='%s' % rrdfilepath + rrdfilename
                    txtfile='%s' % txtfilepath + txtfilename
                    rrd2txtcmd='rrdtool fetch %s' % rrdfile + ' --start now-7day MAX > %s' % txtfile
                    cachcmds="sed '1,2d;$d'" + " %s" % txtfile + "| sed '/-nan/d' | awk '{  sum += $2 ; average = sum/NR} END { print  average }'"
                    r2t = commands.getoutput(rrd2txtcmd)
                    cre = commands.getoutput(cachcmds)
                    cachmonidata="".join(cre).split("\n")


                    brs = cursor.execute(buffersql,ip.split())
                    brest = cursor.fetchall()
                    bfields = cursor.description
                    brow = 1
                    bcol = 0
                    for brow in range(1,len(brest) +1):
                        for bcol in range(0,len(bfields)):
                            if(bcol != 0):
                                desc = brest[brow - 1][bcol]
                                buf = "".join(desc)
                                brrd = buf[11:]
                                btxt = buf[11:-3]+'txt'
                                buffrrdfile='%s' % rrdfilepath + brrd
                                bufftxtfile='%s' % txtfilepath + btxt
                                brrd2txtcmd='rrdtool fetch %s' % buffrrdfile + ' --start now-7day MAX > %s' % bufftxtfile
                                bufcmd="sed '1,2d;$d'" + " %s" % bufftxtfile + "| sed '/-nan/d' | awk '{  sum += $2 ; average = sum/NR} END { print average }'"
                                brt = commands.getoutput(brrd2txtcmd)
                                bres = commands.getoutput(bufcmd)
                                buffdata="".join(bres).split("\n")

                                lip = ip.split()
                                trs=cursor.execute(memTotal,lip)
                                trest=cursor.fetchall()
                                tfields=cursor.description
                                trow=1
                                tcol=0
                                for trow in range(1, len(trest) + 1):
                                    for tcol in range(0, len(tfields)):
                                        if (tcol != 0):
                                            mtdesc=trest[trow - 1][tcol]
                                            memt="".join(mtdesc)
                                            trrd = memt[11:]
                                            ttxt = memt[11:-3] + 'txt'
                                            memrrdfile='%s' % rrdfilepath + trrd
                                            memtxtfile='%s' % txtfilepath + ttxt
                                            trrd2txtcmd='rrdtool fetch %s' % memrrdfile + ' --start now-7day AVERAGE > %s' % memtxtfile
                                            memtcmd="sed '1,2d;$d'" + " %s" % memtxtfile + "| sed '/-nan/d' | awk '{ sum += $2 ; average = sum/NR} END { print  average/1024 ;print $3/1024}'"
                                            trrs = commands.getoutput(trrd2txtcmd)
                                            memst = commands.getoutput(memtcmd)
                                            memTOdata="".join(memst).split("\n")


                                    memData = memTOdata+buffdata+cachmonidata
                                    print(lip,memData)
				    memData = map(eval,memData)
				    print memData
                                    buffer_cached=memData[0]-memData[2]-memData[3]
                                    bcachpercent=round((float(buffer_cached / memData[1])) * 100, 2)
                                    list_Bcachpercent=(str(bcachpercent)+'%').split()+ip.split()
                                    #print list_Bcachpercent
                                    cacrest = cursor.execute(upCachp,list_Bcachpercent)
                                    #print cacrest
                                    conn.commit()
                                    list_buffer_cached=(str(round(buffer_cached/1024,2))+'M').split()+ip.split()
                                    #print 'list_buffer_cached:',list_buffer_cached

                                    cacrest = cursor.execute(upCached,list_buffer_cached)
                                    #print cacrest
                                    conn.commit()

	conn.close()
