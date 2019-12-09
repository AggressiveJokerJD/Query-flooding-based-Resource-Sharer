<b><font size =10>README</font></b>

## 1.实验环境

---

语言：Python

版本：Python 3.7.3

包含外部包：func_timeout 4.3.5

实验名称：Query-flooding-based Resource Sharer

## 2.具体的操作

---

<font color=red>提示，这个操作步骤是标题4.运行过程的一个简洁版，标题4将对下面的第六点进行详细说明,如下步骤即可完成使用，1-5步骤为说明和预操作，步骤6为具体使用过程</font>

1. 安装符合版本的Python

  2. 安装外部包func_timeout，使用命令<code> pip install func-timeout </code>

  3. 其中有10个以IP命名的文件夹(127.0.0.1,127.0.0.2...),每个文件夹下有一个Resources文件夹，用以存放该节点的资源。

  4. 在每个节点文件夹的Resources文件夹下添加自己想要的文件，每个节点下初始包含一张特定的.jpg文件，如果想要添加其他的文件，那么自行添加即可。

  5. 整个testP2P.bat中定义的网络的整体结构如下图所示:

     ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E7%BD%91%E7%BB%9C%E7%BB%93%E6%9E%84%E5%9B%BE.png)

     <font color=red>解释：其中有连线的表示相连，反之不能，而每个节点发出的搜索消息的TTL=3，那么如果超出了TTL，那么将搜索不到资源，例如127.0.0.5到127.1.0.2的最短路径为4，所以127.0.0.5请求127.1.0.2的独有文件的话，将返回超市消息，并告知文件不存在</font>

  6. 具体使用步骤：简略：打开testP2P.bat-->选择一个窗口，输入搜索提示符1-->输入文件名-->等待提示消息之后完成一次查询-->选择窗口...

     1. 打开testP2P.bat，然后将打开10个cmd窗口，分别表示不同节点，每个cmd都有输出说明当前节点的IP
     2. 然后输入查询提示符1，开始查询<font color=red>&emsp;&emsp;注意：请不要输入1除外的信息，否则会产生中断</font>
     3. 输入想要查询的文件名
     4. 直到输出更新之后的资源列表(表示查询成功)或者TimeOut!!!消息(表示查询失败)之后，然后可以重复进行b,c,d步骤<font color = red>在没有输出提示消息时不要连续输入以免出现问题,orz...</font>

     

     

## 3.代码解析

---

### 1).py文件

---

- > Client.py 
  >
  > 包含函数TcpClient,是当查询到资源之后，保持资源的节点通过启动TcpClient来将自己的资源传送到查询资源的初始节点

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/TcpClient.png)

- > Server.py
  >
  > 包含TcpServer函数，是当一个节点开始查询之后，Peer会开启TcpServer用来监听是否有Tcp连接，连接之后就可以进行文件接收功能

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/TcpServer.png)

- > Peer.py
  >
  > 包含节点类(Peer)，属性有IP,TcpPort,UdpPort,ifopenTcp,PeerList,ResourceList
  >
  > 函数有\__init__构造函数，初始化Peer节点
  >
  > List_Peer函数，用来将文件夹中的Peer_List.txt中的当前节点的相连节点读取到PeerList中
  >
  > List_Resource函数，将文件夹中的资源读取出来存储到当前节点的资源列表中
  >
  > Search_Resource函数，搜索自己的资源列表，查询是否存在满足要求的文件，存在则返回资源在列表中的位置(非-1)，不存在则返回-1

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/Peer.png)

  > UdpServer函数  当前Peer初始化后，启动UdpServer进行监听，如果别的Peer传输了消息并且消息可达当前Peer，那么当前节点就可以处理消息并进行操作(包括检测资源，传递消息，传送资源)

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/UdpServer.png)

  > UdpClient函数  可以发出查询或者转发其他Peer的消息等功能

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/UdpClient.png)

  > Search函数 控制节点的搜索资源的函数，当输入标识1时将要进入搜索，然后输入想要搜索的文件的名字即可进行查询，如果搜索超时，那么将输出提示信息，搜索到资源之后进行下载

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/Search.png)

  > 一个测试，运行Peer.py的时候会运行这里的代码，主要有初始化节点，查询功能（Search和UdpClient），监听（UdpServer）

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/main.png)

- > common_operation.py
  >
  > Send_File函数 就是用来发送文件的函数

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/Send_File.png)

  > Receive_File函数 就是用来发送文件的函数

  ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/Recv_File.png)

### 2)资源文件

---

&emsp;&emsp;资源文件都是存放再以节点的IP命名的文件夹下，包括:

- > Resources文件夹
  >
  > 存放的是该节点拥有的资源，从别的节点下载的资源也存放在该文件夹下，也用于更新节点的ResourceList

- > Peer_List.txt
  >
  > 存放的是与当前节点相连接的节点的IP和UdpPort，用于初始化PeerList

### 3)批处理

---

&emsp;&emsp;testP2P.bat:这个是一个批处理文件，就是批量的建立Peer节点，并且批量的初始化Peer节点，运行这个.bat文件会打开10个cmd窗口，每个窗口运行一个Peer节点，然后就可以进行文件传输了。

> 命令:打开cmd运行Peer.py,然后输入每个节点的IP，TcpPort,UdpPort
>
> ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/testP2P.png)
>
> 展示:图钟展示了每个Peer.py运行之后的效果图，如果想新加入节点，那么就在testP2P.bat中加入如上图命令，然后新输入一个Peer的初始化变量，然后创建一个新IP命名的文件夹，文件夹中放入Resources文件夹和一个Peer_List.txt，Peer_List.txt中写入与新节点相连的已经存在的IP，UdpPort即可
>
> ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/testP2P%E6%95%88%E6%9E%9C%E5%B1%95%E7%A4%BA.png)

## 4.运行过程

---

步骤：

  1. 安装符合版本的Python

  2. 安装外部包func_timeout，使用命令<code> pip install func-timeout </code>

  3. 其中有10个以IP命名的文件夹(127.0.0.1,127.0.0.2...),每个文件夹下有一个Resources文件夹，用以存放该节点的资源。

  4. 在每个节点文件夹的Resources文件夹下添加自己想要的文件，每个节点下初始包含一张特定的.jpg文件，如果想要添加其他的文件，那么自行添加即可。

  5. 整个testP2P.bat中定义的网络的整体结构如下图所示:

     ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E7%BD%91%E7%BB%9C%E7%BB%93%E6%9E%84%E5%9B%BE.png)

     <font color=red>解释：其中有连线的表示相连，反之不能，而每个节点发出的搜索消息的TTL=3，那么如果超出了TTL，那么将搜索不到资源，例如127.0.0.5到127.1.0.2的最短路径为4，所以127.0.0.5请求127.1.0.2的独有文件的话，将返回超市消息，并告知文件不存在</font>

  6. 在保证之前的操作完成后，运行testP2P.bat即可进行操作。

     - > 首先会批量的打开10个节点并运行，每个节点显示信息如下：![运行示例1](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/127.0.0.1%E6%98%BE%E7%A4%BA.png)
       >
       > 1. 在这个图片中首先显示该节点的相关信息，分别为IP，TcpPort，UdpPort。
       >
       > 2. 然后显示为Resources：当前Peer包含的资源文件
       >
       > 3. Udp消息监听启动提示
       >
       > 4. 提示当前可以输入1来表示当前节点想要搜索文件

     - > 如果你想搜索资源，那么输入1即可：
     >
       > ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%89%8D.png)
     >
       > ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%90%8E.png)
       >
       > 图中显示在127.0.0.6节点的窗口中，输入1，然后输出<code>Please input the filename you want to search...</code>提示符，然后再输入你想要查找的文件名，图中输入为<code>yellowmonkey.jpeg</code>(<font color=red>注意这里必须输入文件的全称，要在文件名后面添加文件类型，不然无法找到</font>),再每次接收完文件之后都会输出Peer更新之后的资源列表，就如图中的最开始的时候输出的资源列表中不包含<code>yellowmonkey.jpeg</code>，之后输出的资源列表包含该文件。而在该Peer的文件夹中也确实出现了<code>yellowmonkey.jpeg</code>该文件
       >
       > <font color= red>上图是成功传输文件之后显示的消息，其中包括多条提示消息，因为多线程的原因，没有办法完美控制输出流，所以显得比较乱，在这里做一个说明：如果是成功传输完文件之后，直到输出更新之后的资源列表算是完全完成了一次查询，在没有输出资源列表时不要连续输入以免出现问题</font>
     
     - > 接下来演示超时的情况，超时主要分为两种情况:
       >
       > - > 第一种情况是搜索的资源不在整个网络的每个节点的资源文件夹下：
       >   >
       >   > ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E4%B8%8D%E5%AD%98%E5%9C%A8%E7%9A%84%E6%96%87%E4%BB%B6%E6%9F%A5%E8%AF%A2%E8%B6%85%E6%97%B6.png)
       >   >
       >   > 输入搜索提示符1之后输入文件名为nothisfile的文件，这个文件不存在于整个网络的任何一个节点的资源文件夹下，所以在输入文件名后的5s钟输出TIMEOUT!!!信息
       >
       > - > 第二种情况是搜索的资源存在于超出自己节点距离3以上的节点文件夹下：
       >   >
       >   > ![](https://study-image-1259719447.cos.ap-chengdu.myqcloud.com/%E8%AE%A1%E7%BD%91/%E8%B6%85%E5%87%BATTL%3D3%E7%9A%84%E6%9F%A5%E8%AF%A2%E8%B6%85%E6%97%B6.png)
       >   >
       >   > 上图搜索文件只存在于192.1.0.2的资源文件夹下，然后使用127.0.0.5去搜索，因为根据上面的网络结构，127.1.0.2和127.0.0.5之间的距离为4，所以127.0.0.5无法搜索到127.1.0.2的文件，在五秒之后输出TIMEOUT!!!信息
       >
       >   <font color=red>注意：和文件传输成功一样，因为线程的原因，很难完美控制输出流，所以输出消息显得很乱，在这里做一个说明：如果传输文件失败，直到输出TimeOut!!!的消息才算该次查询完成，在没有输出TimeOut!!!消息时不要连续输入以免出现问题</font>
