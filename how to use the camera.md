首先按照官方教程将各种依赖包装好（如果中间报错后面无法正常进行，一定要正确安装）

官方教程：[Linux] The Imaging Source GigE Series of teaching-中文版_2019_02_21更新.pdf

下载链接：https://pan.baidu.com/s/16aJex15YFu0ZkAndbTPGig  密码：cao2

一、只有一个相机的情况（相对简单，也是现在比较稳定的使用方法）

1、修改相机IP地址：

插上连接相机的网线后，选择网络，点击edit connection，选择相机所连接的网络，选择ipv4 settings，将模式（mothod）选择为手动（manual）：

在address栏处点击add添加一个网络地址，设置如下：

address：169.254.a.b    （这里a一般为3，b为除1以外0至255内任意的整数）

netmask：255.255.255.0

gateway：255.255.255.0

保存退出

2、检测是否连上相机

打开终端（terminal），输入命令：Camera-ip-conf -l

若看到有相机，则表示相机连接成功，可以进行接下来的操作，否则再次检查1中地址是否修改正确，保存后，重启电脑

只要检测到相机，就算会有报错也不会对接下来的操作有影响

3、固定IP的设定

打开terminal分别输入下列命令：

camera-ip-conf set ip=192.168.a.x subnet=255.255.255.0 gateway=0.0.0.0 -s <camera_id>

camera-ip-conf set static=on -s <camera_id>

camera-ip-conf forceip ip=192.168.a.x subnet=255.255.255.0 gataway=0.0.0.0 -s <camera_id>

（注意：命令中的a必须与步骤1中设定的IP地址中的b相同，x则不能与b相同，参数<camera_id>指的是相机的序列号，连接对应的相机要输入对应的序列号，每台相机的序列号都不一样，全局相机的序列号是41814186，机械臂上相机的序列号是21814614）

中间可能会有一些警告报出，但并不影响对相机的操作

固定IP设定好之后即可进行接下来的操作

----------------------------------------------------------------------------------------------------------------------------

注意：步骤3只需要在新相机上运行一次即可，步骤3的作用是固定相机的ip地址，运行之后，你在set后面设置的ip、subnet、gateway都会永久写入序列号为<camera_id>的相机中，待下一次需要再使用时，在步骤1中对网口设置的ip地址需要与第一次使用步骤3时对对应相机设置的ip地址的前三部分相同，例如：第一次运行步骤3时对camera_id 为123456的相机设置了abc.def.ghi.x的ip地址，那么，以后再需要调用相机的时候就不需要再进行步骤3了，但是必须确定在步骤1中设置的网口ip地址是：abc.def.ghi.y，其中y不能和之前设置的x相同，即确保相机和主机在同一网段内（2019/4/2,今天我运行了步骤3,将两个相机的ip都固定住了，全局相机的ip地址是192.168.15.12，机械臂相机的ip地址是192.168.14.13，具体的我可能记反了，但是是这两个ip地址肯定是没错的，运行的时候如果不对就换一下就好）

建议修改ip地址在windows下使用相机官方给的程序进行修改，点开开始菜单，在gige image

4、相机的开启与关闭

在terminal中输入以下命令即可进行对应的操作

gige-daemon start      打开相机（只有打开了相机才能在TIS库中调用相机）

tcam-ctrl -l                 查看当前连接的相机的型号、序列号

tcam-ctrl -f                 查看当前连接的相机的输出格式和解析度（一般指帧数(fps)和分辨率，全局相机分辨率为1280*960，机械臂上的相机分辨率为1600*1200，顺序我可能记反了，不过也可以用这个命令查出来）

gige-daemon stop      关闭相机

----------------------------------------------------------------------------------------------------------------------------

完成步骤1到步骤4就算完成了电脑和相机的连接，接下来是在主机python程序中如何调用相机完成一些基本的操作

5、准备需要用到的文件和一些python库

文件：TIS.py  TIS.pyc

在python程序中需要import的库：

import TIS

import cv2

TIS.py需要的库：gi、numpy、time

gi库的安装参考链接：https://packages.ubuntu.com/trusty/python3-gi

按照链接所列依赖包依次安装好即可

6、在python程序中建立一个TIS类对象

例如：try_tiscamera=TIS.TIS("21814614",1600,1200,15,True)

这句代码中：

try_tiscamera是TIS类对象名

TIS.TIS是个TIS类的构造函数，用于构造一个TIS类对象

参数"21814614"指的是TIS类对象所连接相机的序列号，在前面的步骤中可获得

第二、第三个参数指的是所连接相机的分辨率参数，第一个是宽（width）第二个是高（height）

第四个参数是指所选择输出的帧率（fps)，帧率只能选择在步骤4中通过tcam-ctrl -f命令所得到的帧数（如果有好几种帧率，选其中一种即可）

第五个参数是选择输出图像的色彩格式，True = 8 bit color, False = 8 bit mono ，一般选True即可

建立TIS类对象后，可以通过该类对象对相机进行操作

7、对相机的基本操作流程

7.1 启动相机，使相机开始输出数据流（Start the pipeline so the camera streams）必须第一个进行

这里可以直接使用之前建立的TIS类对象进行操作：

try_tiscamera.Start_pipeline()

7.2 让相机抓取图片

try_tiscamera.Snap_image(t)：延时t秒后让相机抓取一张图片，保存在TIS类对象try_tiscamera.img_mat内参中，如果操作成功则返回True,否则返回False

注意：刚刚创建TIS类对象时，TIS.img_mat的值为None（空），若抓取图像失败，则这里的值会保持原来的值不变，若img_mat原先已经保存了一张图片，则抓取失败时这里仍然会保留原来的值不变

7.3  获取相机抓取的图片

通过如下代码即可获得在7.2中获得的try_tiscamera中抓取的图片

image=try_tiscamera.Get_image()

这句代码的作用就是将try_tiscamera.img_mat赋值给image对象，此时image对象就获得了刚刚抓取的图像可以进行各种图像操作了

例如：通过cv2.imwrite('camera.jpg',image)将image中的图片写入camera.jpg文件中保存

7.4  关闭相机

使用完相机后，通过以下命令关闭TIS类对象所连接的相机

try_tiscamera.Stop_pipeline()

8、实现对相机的实时监控

通过7中的一些基本操作可以完成对相机的所拍视频的实时输出，这个操作使用一个while循环实现：

lastkey=1

cv2.namedWindow('Window')   #创建一个窗口用于输出图片

while lastkey==1

     if try_tiscamera.Snap_image(1) is True:    #每秒钟抓取一张图片，若抓取成功则进行接下来的操作
     
          image=try_tiscamera.Get_image()      #获取抓取到的图片
          
          cv2.imshow('Window', image)            #将获取到的图片显示在创建的窗口中
          
#关闭连接并摧毁窗口

try_tiscamera.Stop_pipeline()

cv2.destroyAllwindows()
