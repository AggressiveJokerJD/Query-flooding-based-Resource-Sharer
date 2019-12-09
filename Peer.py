'''
节点的存放类，里面应该运行一个Server和一个Client
节点应该包含自己的Server的IP地址和Port端口号
节点创建时应该直接运行Server，当需要进行下载资源的时候，开启新线程再启动Client？
下载文件保存到相应文件夹
'''

'''
TCPClient 用到参数:
    Server IP,Port，filepath
TCPServer 用到参数：
    IP，Port

UDPClient 作用：
    1.发送消息，包含from（IP,Port）和要搜索的文件名和传播List给相连接的节点
    2.如果Server接收到消息，那么将
'''

import os
import Client
import Server
import threading
import socket
import sys


TTL = 3

class Peer(object):

    '''
    参数作用：
        1.IP 就是节点IP
        2.TcpPort 就是Tcp端口号
        3.UdpPort 就是Udp端口号
        4.ifopenTcp 标识Tcp连接开始的信号，开启则不再重复开启
        5.PeerList 与该节点相连接的节点列表
        6.ResourceList 该节点的资源列表
    '''
    def __init__(self,IP,TcpPort,UdpPort):
        self.IP = IP
        self.TcpPort = TcpPort
        self.UdpPort = UdpPort
        self.ifopenTcp = 0

        self.PeerList ={}
        self.ResourceList = []

    def List_Peer(self,IP):
        peerpath = './{0}/Peer_List.txt'.format(IP)
        f = open(peerpath,'r')
        list = f.readlines()
        for line in list:
            peerline = line.strip().split(':',1)
            self.PeerList[peerline[0]] = int(peerline[1])
        # print(str(self.PeerList))

    def List_Resource(self,IP):
        resourcepath = './{0}/Resources'.format(IP)
        self.ResourceList = os.listdir(resourcepath)
        # print(self.ResourceList)

    def Search_Resource(self,filename):
        ifhaveresource = -1
        for res in self.ResourceList:
            if res == filename:
                ifhaveresource += 1
                return ifhaveresource
            else:
                ifhaveresource += 1
        return -1

    '''
    函数作用:
        在当前Peer初始化完成之后，就开始运行UdpServer来监听其他Peer发出的查询消息
    '''
    def UdpServer(self):
        try:
            udps = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            udps.bind((self.IP,self.UdpPort))
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        print("UdpServer:wating for massage...")
        while True:
            # print(self.ResourceList)
            filehead,address = udps.recvfrom(1024)
            filehead = eval(filehead.decode('utf-8'))
            '''
            这里应该查询自己的资源文件夹看是否有文件名相同的
            如果有的话，就开启TcpClient传输数据,地址是addr
            '''
            fromip = filehead['fromIP']
            if not self.Search_Resource(filehead['filename']) == -1:
                # print("run at here")
                Send_Thread = threading.Thread(target=Client.TcpClient,args=((filehead['sourceIP'],filehead['sourcePort']),filehead['filename'],self.IP))
                Send_Thread.start()
            else:
                if filehead['ttl'] > 0:
                    filehead['ttl'] -= 1
                    for peerip in self.PeerList.keys():
                        if peerip != fromip:
                            # print(filehead['filename'],(peerip, self.PeerList[peerip]), filehead['sourceIP'],
                            #                filehead['sourcePort'], self.IP, filehead['ttl'])
                            self.UdpClient(filehead['filename'], (peerip, self.PeerList[peerip]), filehead['sourceIP'],
                                           filehead['sourcePort'], self.IP, filehead['ttl'])


    '''
    参数说明:
        1.addr 需要udpsocket绑定的地址，发送消息到这个地址
        2.sourceIP 这条消息的最初是的来源IP
        3.sourcePort 这条消息的最初的来源的Port
        4.fromIP 传给你这条消息的Peer的IP(用以判断是否要传送回去，避免回环)
        5.ttl 当前消息的存活周期
    函数作用:
        1.发出查询消息:首次发出的时候(也就是TTL==3的时候)，会发出查询信息给地址为addr的节点，并且开启一个线程运行
          TcpServer以监听是否查询到想要的file，如果查询到那么接收file到自己的Resources文件夹下，如果查询超时则输
          出提示信息'Search Timeout!!'.
        2.转发查询的消息:不是首次发出(TTL!=3),会转发查询信息给地址为addr的节点.
    '''
    def UdpClient(self,filename,addr,sourceIP,sourcePort,fromIP,ttl):
        try:
            udps = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            udps.connect(addr)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        if ttl == 3 and self.ifopenTcp == 0:
            self.ifopenTcp = 1
            # print(self.ifopenTcp)
            Recv_Thread = threading.Thread(target=Server.TcpServre,args=(sourceIP,sourcePort,self))
            Recv_Thread.start()
            # filename = input("Please input filename you want to search...\n")
        filehead = {'filename':filename,'sourceIP':sourceIP,'sourcePort':sourcePort,'fromIP':fromIP,'ttl':ttl}
        udps.sendto(str(filehead).encode('utf-8'),addr)
        udps.close()

    def Search(self):
        ifsearch = input("Please input 1 if you want to search file...\n")
        # print("run at here")
        # print(ifsearch == 1)
        while int(ifsearch) == 1:
            filename = input("Please input the filename you want to search...\n")
            for peer in self.PeerList.keys():
                self.UdpClient(filename, (peer, self.PeerList[peer]), self.IP, self.TcpPort, self.IP, 3)
            self.ifopenTcp = 0
            print("Has sent the search message...")
            print("Please wait for search until TIMEOUT or RECEIVE message be print...")
            ifsearch = input("Then you can input 1 if you want to search next file...\n")



if __name__ == '__main__':
    print("IP: {0}  TcpPort:{1}  UdpPort:{2}  has running...".format(sys.argv[1],sys.argv[2],sys.argv[3]))
    # peer = Peer('127.0.0.1',3366,3367)
    peer = Peer(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    peer.List_Peer(peer.IP)
    peer.List_Resource(peer.IP)
    #以上为初始化节点
    print("Resourse:{0}".format(peer.ResourceList))
    t = threading.Thread(target=peer.Search)
    #查询
    t.start()
    peer.UdpServer()
    #监听






