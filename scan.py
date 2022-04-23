"""
支持命令行的端口扫描器
用法:
python scan.py --help  查看帮助
python scan.py --version 查看版本
python scan.py 目标ip [目标端口 | 目标端口列表，使用逗号分隔 | 目标端口范围]
"""

import socket, sys


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


# 判断端口是否打开
def is_open(ip, port):
    scan_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    scan_socket.settimeout(2)  # 设置连接超时时间
    try:
        scan_socket.connect((ip, port))
        return True
    except:
        return False


# 扫描端口列表
def scan(ip, portlist):
    for port in portlist:
        if is_open(ip, port):
            color_print("%s host %s port is open" % (ip, str(port)), 1)
            # print("%s host %s port is open" % (ip, str(port)))
        else:
            color_print("%s host %s port is close" % (ip, str(port)), 2)
            # print("%s host %s port is close" % (ip, str(port)))


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
    defaultPort = [20, 21, 22, 23, 80, 443, 3306, 3389,6379]
    str1 = sys.argv[1]  # 获取第一个参数
    # 如果只有一个参数
    if len(sys.argv) == 2:
        if str1[0] == '-':
            option = str1[2:]
            # 版本
            if option == 'version':
                print("当前版本号是1.0.0")
            # 帮助
            elif option == 'help':
                print('帮助:python scan.py ip [port | port1-port2]')
            sys.exit()
        # 只有一个ip参数，扫描默认端口  例如 python scan.py 127.0.0.1
        scan(str1, defaultPort)

    # 有两个参数，可能是ip加端口列表，也可能是ip加端口范围
    elif len(sys.argv) == 3:
        str2 = sys.argv[2]
        portList = []
        # python scan.py 127.0.0.1 80,89
        if ',' in str2:
            p = str2.split(',')
            for port in p:
                portList.append(int(port))
            scan(str1, portList)
        # pyton scan.py 127.0.0.1 80-89
        elif '-' in str2:
            p = str2.split("-")
            start_port = int(p[0])
            end_port = int(p[1])
            lscan(str1, start_port, end_port)
        # 扫描单个端口  python scan.py 127.0.0.1 80
        else:
            portList.append(int(str2))
            scan(str1, portList)


if __name__ == '__main__':
    main()
