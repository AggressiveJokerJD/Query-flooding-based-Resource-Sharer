'''
TcpClient:
    1.就是传输文件即可

UdpClien:
    1.发送洪范即可
'''

import socket
import common_operation
import sys
import Server
import threading

SIZE = 1024

'''
参数说明：
    1.addr 为要传输文件到的地址，也就是发送Udp查询的源地址
    2.filename 为所要传输的文件的名字
    3.IP 为当前Peer的IP，传入Send_File()以打开当前Peer的资源文件夹
'''
def TcpClient(addr,filename,IP):
    try:
        Cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        Cs.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        Cs.connect(addr)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    common_operation.Send_File(Cs,filename,IP)
    print("TcpCilent:{0} send over".format(filename))
    return



