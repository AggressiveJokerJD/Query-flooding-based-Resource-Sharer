'''
1.包括洪范
    1）从源发出请求，传给他的相连接的节点，设置TTL为3
    2）相连节点再以IP地址命名的文件夹中的Peer_List.txt中包含节点中读取相连节点
    3)
2.文件传输？
    1)首先用socket连接
    2）获取文件名
    3）将文件名和文件的大小包装传输到Server---struct.pack(format,data...)
    4）然后读取文件，传输相应的文件到Server
3.文件接收
    1）接收Client传输的文件名和文件大小---filehead
    2）然后读取文件直到读取完整整个文件---正好是等于传送file的大小时停止
    3）Peer应该有一个自己的Server IP相同名的文件夹，存储Peer_List，和一个Recv文件夹存储
'''

import struct
import os

SIZE = 1024

'''
参数说明:
    1.Csock 发送文件的套接字，也就是调用Send_File的TcpCilent的套接字
    2.filepath 要发送的文件的名字
    3.IP 当前节点的IP，用来定位filepath的具体地址
函数作用：
    就是发送一个文件，首先发送一个文件头，是一个'128sq'类型的数据，包含文件的路径的bytes类型和要传输的文件的大小(按流的形式的大小),然后打开路径
    开始按照SIZE大小进行发送，直到发送完为止
'''
def Send_File(Csock,filepath,IP):
    newfilepath = './{0}/Resources/{1}'.format(IP,filepath)
    filehead = struct.pack(b'128sq',bytes(os.path.basename(newfilepath),encoding='utf-8'),os.stat(newfilepath).st_size)
    Csock.send(filehead)

    fileopen = open(newfilepath,'rb')

    while True:
        data = fileopen.read(SIZE)
        if not data:
            break
        Csock.send(data)

''' 
参数说明：
    1.IP 接收文件的节点的IP，用来定位到当前节点的资源文件
    2.Ssock 接收文件的服务器的套接字
函数作用：    
    接收到服务器的socket，然后接收Client端发出的filehead，然后根据给定的格式进行解压，
    提取出文件名和文件大小，一直接收到文件大小为止
'''
def Receive_File(IP,Ssock):
    while True:
        fileinfo_size = struct.calcsize('128sq')
        filehead = Ssock.recv(fileinfo_size)
        if filehead:
            filename,filesize = struct.unpack('128sq',filehead)
            fn = filename.decode().strip('\x00')
            new_filename = './{0}/Resources/{1}'.format(IP,fn)

            recv_size = 0
            recv_fileopen = open(new_filename,'wb')

            while not recv_size == filesize:
                if filesize - recv_size > 1024:
                    data = Ssock.recv(SIZE)
                    recv_size += len(data)
                else:
                    data = Ssock.recv(SIZE)
                    recv_size = filesize
                recv_fileopen.write(data)
            print("{0} has received...".format(fn))
            recv_fileopen.close()
        break





