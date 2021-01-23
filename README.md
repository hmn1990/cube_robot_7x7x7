# cube_robot_7x7x7

#### 介绍
使用树莓派控制的魔方机器人，可以在平均5-6分钟的时间内完成7阶魔方的还原。
使用C + Python开发，含有结构设计、软件部分，实物照片，演示视频。
算法使用rubiks-cube-NxNxN-solver，可还原任意阶数魔方，在原版基础上略有修改。

#### 系统架构
树莓派--+--步进电机驱动器--升降控制电机
       +--升降零点微动开关
       |
       +--步进电机驱动器--翻转控制电机
       +--翻转零点光电开关
       |
       +--步进电机驱动器--旋转控制电机	
       +--旋转零点光电开关
       |
       +--USB摄像头（120度视角）
       +--键盘、鼠标、显示器
       +--USB转mSATA--固态硬盘（可选配置，对提高求解速度有很大的作用）

#### 演示视频：
七阶魔方
http://v.youku.com/v_show/id_XNTA3NDcyNjU5Ng==.html?x&sharefrom=android&sharekey=1a05666036d4e04ea54c2c59a5a633d63
三阶魔方
http://v.youku.com/v_show/id_XNDg5NTM2OTg5Mg==.html?x&sharefrom=android&sharekey=72dc6125e1c21ec2b96ba7e84085a9bb3

#### 配置与运行步骤：
1、安装python3-opencv
sudo apt-get install python3-opencv

2、安装ckociemba
cd kociemba/
make
sudo make install

3、安装rubiks-cube-NxNxN-solver（该版本相对于原始版本有修改，添加了边计算边输出中间结果的功能，去除了对python venv的需求）
make init
./rubiks-cube-solver.py --state DBDBDDFBDDLUBDLFRFRBRLLDUFFDUFRBRDFDRUFDFDRDBDBULDBDBDBUFBUFFFULLFLDURRBBRRBRLFUUUDUURBRDUUURFFFLRFLRLDLBUFRLDLDFLLFBDFUFRFFUUUFURDRFULBRFURRBUDDRBDLLRLDLLDLUURFRFBUBURBRUDBDDLRBULBULUBDBBUDRBLFFBLRBURRUFULBRLFDUFDDBULBRLBUFULUDDLLDFRDRDBBFBUBBFLFFRRUFFRLRRDRULLLFRLFULBLLBBBLDFDBRBFDULLULRFDBR
第二个步骤很慢，需要联网下载大量数据，解压后需要占用6.2GB空间。

4、修改/boot/cmdline.txt 在末尾添加isolcpus=3，然后重启，可选步骤，可改善运行时卡顿的问题


5、编译并且加载内核模块，在此之前请安装好linux内核头文件
cd cube_robot_kernel_module
make
sudo make load
cd ..
如需调整电机旋转速度，修改step_moter.py，make table后重新编译内核模块

6、运行主程序
./cube_robot.py
等待出现预览画面后，放入魔方，按空格键开始还原，ESC退出。




