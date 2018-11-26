# coding:utf8


from d_linux_export.conStant import Constant
class Test():


    def pwinhost(self):
        c=Constant()
        wlist = c.winhosts().split(',')
        d = '172.16.41.3'
        if(d in wlist):
            print d




if __name__ == '__main__':
    t = Test()
    t.pwinhost()