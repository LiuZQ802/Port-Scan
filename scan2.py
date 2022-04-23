# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Project :  main.py
@File    :  scan2
@Author  :  刘子琦
@Data    :  2022/4/23
@Description:
    高级命令行的端口扫描器
"""
import socket
from optparse import OptionParser

# 带颜色的输出
def color_print(message, level=0):
    color_common = ''  # 正常输出
    color_green = '\033[1;32m[开放]'  # 绿色输出
    color_red = '\033[1;31m[关闭]'  # 红色输出

    if level == 0:
        print(color_common + message)
    elif level == 1:
        print(color_green + message)
    else:
        print(color_red + message)

    print('\033[0m')
    pass


#判断是否开通端口
def is_open(ip,port):
    soc=socket.socket()
    soc.settimeout(1)
    try:
        soc.connect((ip,port))
        return True
    except:
        return False

#扫描端口列表
def scan(ip,portList):
    for port in portList:
        if is_open(ip,port):
            color_print("%s host %s port is open" % (ip, str(port)), 1)
        else:
            color_print("%s host %s port is close" % (ip, str(port)), 2)

# 扫描端口范围
def lscan(ip, start, end):
    for port in range(start, end + 1):
        if is_open(ip, port):
            color_print("%s host %s port is open" % (ip, str(port)), 1)
            # print("%s host %s port is open" % (ip, str(port)))
        else:
            color_print("%s host %s port is close" % (ip, str(port)), 2)
            # print("%s host %s port is close" % (ip, str(port)))



def main():
    usage="scan2.py -i ip地址 [-p 端口]"
    parse=OptionParser(usage=usage)
    parse.add_option("-i","--ip",type="string",dest="ipaddress",help="your target ip here")
    parse.add_option("-p","--port",type="string",dest="port",help="your target port here")
    (options,args)=parse.parse_args()

    ip=options.ipaddress
    port=options.port

    defaultport=[20,21,22,23,80,443,3306,3389]


    if not port:
        scan(ip, defaultport)
    elif ',' in port:
        port=port.split(',')
        a=[]
        for p in port:
            a.append(int(p))
        scan(ip,a)
    elif '-' in port:
        port=port.split('-')
        start=int(port[0])
        end=int(port[1])
        lscan(ip,start,end)
    elif port=='dafault':
        scan(ip,defaultport)
    elif port=='all':
        lscan(ip,1,65535)

    pass

if __name__=='__main__':
    main()