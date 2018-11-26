# coding:utf8
import datetime

class Constant(object):
    #IPAddress
    def getHost(self):
        host='172.16.50.14'
        return  host

    #服务器用户名
    def getUser(self):
        user='root'
        return user

    #服务器密码
    def getPwd(self):
        pwd='1o-8Dengyu2'
        return pwd

    #DB名称
    def getDbName(self):
        db='cacti'
        return db

    #DB用户名
    def getDbUser(self):
        dbuser = 'cacti'
        return dbuser

    def getDbPwd(self):
        dbpwd = 'cacti'
        return dbpwd

    def getRrdPath(self):
        rrdfilepath='/var/www/html/cacti/rra/'
        return rrdfilepath

    def getTxtPath(self):
        txtfilepath='/home/rrdData/'
        return txtfilepath

    def getXname(self):
        xname='CactiWeekMonitorData_'+datetime.datetime.now().strftime('%Y%m%d')+'.xls'
        return xname

    def mailuserlist(self):
        #mailusers=' huazhanghui@pb-station.com,liuyingnan@pb-station.com,dongruijie@pb-station.com'
        mailusers=' huazhanghui@pb-station.com'
	#mailusers=' huazhanghui@pb-station.com,liuyingnan@pb-station.com'
        return mailusers

    def reportpath(self):
        reportpath='/home/reports/'
        return reportpath

    def getSeCpuSql(self):
        cpusql='select hostname,data_source_path from data_local,data_template_data, host ' \
                'where data_local.id = data_template_data.local_data_id ' \
                'and host.id = data_local.host_id ' \
                'and name = \'|host_description| - CPU Usage - System\' ' \
                'and hostname in (select hostname from host)'
        return cpusql

    def getSeDiskSql(self):
        disksql='select hostname,data_source_path ' \
                  'from data_local,data_template_data, host ' \
                  'where data_local.id = data_template_data.local_data_id ' \
                  'and host.id = data_local.host_id  ' \
                  'and name = \'|host_description| - Used Space - /\' ' \
                  'and hostname in (select hostname from host)'
        return disksql

    def getSeMemSql(self):
        memsql='select hostname,data_source_path ' \
                 'from data_local,data_template_data, host ' \
                 'where data_local.id = data_template_data.local_data_id ' \
                 'and host.id = data_local.host_id  ' \
                 'and name = \'|host_description| - Used Space - Physical memory\' ' \
                 'and hostname in (select hostname from host)'
        return memsql

    def getSeSwapSql(self):
        swapsql='select hostname,data_source_path ' \
                'from data_local,data_template_data, host ' \
                'where data_local.id = data_template_data.local_data_id ' \
                'and host.id = data_local.host_id  ' \
                'and name = \'|host_description| - Used Space - Swap space\' ' \
                'and hostname in (select hostname from host)'
        return swapsql

    def getHomeSql(self):
        homesql='select hostname,data_source_path ' \
                'from data_local,data_template_data, host ' \
                'where data_local.id = data_template_data.local_data_id ' \
                'and host.id = data_local.host_id  ' \
                'and name = \'|host_description| - Used Space - /home\'' \
                'and hostname in (select hostname from host)'
        return homesql

    def getCached(self):
        cached='select hostname,data_source_path ' \
               'from data_local,data_template_data,host ' \
               'where data_local.id = data_template_data.local_data_id ' \
               'and host.id = data_local.host_id ' \
               'and name = \'|host_description| - ucd_memCached\'' \
               'and hostname in (select hostname from host)'
        return cached

    def getBuffer(self):
        buffer='select hostname,data_source_path ' \
               'from data_local,data_template_data, host ' \
               'where data_local.id = data_template_data.local_data_id ' \
               'and host.id = data_local.host_id ' \
               'and name = \'|host_description| - ucd_memBuffer\'' \
               'and hostname = %s'
        return buffer

    def getMemtotal(self):
        memTotal='select hostname,data_source_path ' \
                 'from data_local,data_template_data, host ' \
                 'where data_local.id = data_template_data.local_data_id ' \
                 'and host.id = data_local.host_id  ' \
                 'and name = \'|host_description| - Used Space - Physical memory\' ' \
                 'and hostname = %s'
        return memTotal

    def winCpusql(self):
        wincpu='select hostname,data_source_path ' \
               'from data_local,data_template_data, host ' \
               'where data_local.id = data_template_data.local_data_id ' \
               'and host.id = data_local.host_id ' \
               'and name = \'|host_description| - CPU Stats - |query_cpuInstance|\'' \
               'and hostname in (select hostname from host)'
        return wincpu

    def winDisk(self):
        windisk='select hostname,data_source_path ' \
                'from data_local,data_template_data, host ' \
                'where data_local.id = data_template_data.local_data_id ' \
                'and host.id = data_local.host_id ' \
                'and name = \'|host_description| - Used Space - C: Label:  Seri\'' \
                'and hostname in (select hostname from host)'
        return windisk

    def seHostDes(self):
        sehostdes='select host.id,hostname,description,usefor from host,xport_host_info where host.id=xport_host_info.id'
        return sehostdes

    def inHostDes(self):
        inhostdes='insert into xport (ID,Hostname,Description,UseFor) VALUES (%s,%s,%s,%s)'
        return inhostdes

    def upCpuSql(self):
        upcpusql='update xport set CPU_usp= %s WHERE Hostname= %s'
        return upcpusql

    def upDiskSql(self):
        updisksql='update xport set Root_space_usd = %s,Root_space_Total = %s,Root_space_usp = %s WHERE Hostname= %s'
        return updisksql

    def upMemSql(self):
        upmemsql='update xport set Mem_us= %s,Mem_Total = %s,Mem_usp = %s,update_time = %s WHERE Hostname= %s'
        return upmemsql

    def upSwapSql(self):
        upswapsql='update xport set Swap_usd = %s,Swap_Total = %s WHERE Hostname = %s'
        return upswapsql

    def upHomesql(self):
        uphomesql='update xport set Home_usd = %s,Home_Total = %s,Home_usp = %s WHERE Hostname = %s'
        return uphomesql

    def upCached(self):
        upcached='update xport set buffers_cache = %s where Hostname = %s'
        return upcached

    def upCachp(self0):
        upcachedp='update xport set buffers_cache_p = %s where Hostname = %s'
        return upcachedp

    def exportSql(self):
        exsql='select ID,Hostname,Description,CPU_usp,Disk_us,Disk_Total,Disk_usp,Mem_us,Mem_Total,Mem_usp,update_time from xport'
        return exsql

    # def getRrd2TxtCmd(self):
