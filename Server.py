'''
TcpServer作用：
    1.接收文件到自己的IP命名的文件夹下的Resources文件夹下
    2.当UdpClient发出洪范查询之前，就在UdpServer中开启一个线程以运行TcpServer以接收信息
    3.这里应该判断超时，若超时则输出"Time out！..."即可
    4.若接收到Tcp连接（accept）那么，开始接收文件，接收完毕之后输出接收完毕并且关闭Server和接收方的client_socket(一次性使用)
UdpServer作用：
    1.在Peer初始化之后，直接运行开始监听
    2.读取输入，若输入为s/S(Search),则开启一个新的线程运行TcpServer,然后在主线程中开启UdpClient开始洪范
    3.然后如果是接收到别的UdpClient的消息之后，查看自己的资源文件，如果存在则建立一个新的线程，然后建立Tcp连接传输文件
    4.如果自己发出的消息，在已经接收到资源的时候如果接收到别的Tcp请求，则不接受直接断开即可，传输提示消息也可以！！！-----应该放在哪里呢？
'''

import socket
import common_operation
import sys
import func_timeout
from func_timeout import func_set_timeout


SIZE = 1024

'''
参数说明：
   1.IP 当前节点的IP地址，用以绑定Tcp连接
   2.TcpPort 当前节点的Tcp端口号， 用以绑定Tcp连接
   3.Peer 当前节点传入，用以实时更新当前的资源列表（貌似传这个参数就可...我吐了...）
'''
def TcpServre(IP,TcpPort,Peer):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#用来保证Server关闭之后端口号可以重用
        s.bind((IP, TcpPort))
        s.listen(3)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("TcpServer:Wating for connection,ready for receiving file...")
    print("If didn\'t receive any message in 5s, the TcpServer will quit!!!!")
    try:
        sock, addr = receiverTcp(s)
        print("TcpServer：Begin to receive file...")
        common_operation.Receive_File(IP, sock)
        sock.close()
        print("TcpServer:connection has closed")
        Peer.List_Resource(Peer.IP)
        print("Resourse:{0}".format(Peer.ResourceList))
    except func_timeout.exceptions.FunctionTimedOut:
        print("Search TimeOut!!!Don\'t have the resource you wanna search...")
        return

'''
函数作用:
    func_set_timeout改变下面函数的规定执行时间，如果时间超过给定值，
    那么将抛出FunctionTimeOut的异常
'''
@func_set_timeout(5)
def receiverTcp(socket):
    sock,addr = socket.accept()
    return sock,addr


