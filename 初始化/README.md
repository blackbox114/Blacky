#进入写模式
rw

#换源
$sudo sed -i 's|raspbian.raspberrypi.org|mirrors.ustc.edu.cn/raspbian|g' /etc/apt/sources.list

$sudo sed -i 's|//archive.raspberrypi.org|//mirrors.ustc.edu.cn/archive.raspberrypi.org|g' /etc/apt/sources.list.d/raspi.list

$sudo apt-get update

#pqi更新pip源
$pip install pqi

$pqi

$pqi use ustc

#自动对时
$sudo date  --s="2020-11-08 20:42:00"

$sudo apt-get install ntpdate 

#更换为国内对时服务器
$sudo nano /etc/ntp.conf
将
pool 0.debian.pool.ntp.org iburst
pool 1.debian.pool.ntp.org iburst
pool 2.debian.pool.ntp.org iburst
pool 3.debian.pool.ntp.org iburst
更换为
server 1.cn.pool.ntp.org iburst
server 2.cn.pool.ntp.org iburst
server 3.cn.pool.ntp.org iburst
server 0.cn.pool.ntp.org iburst

#下载项目文件
$git clone https://github.com/stanfordroboticsclub/StanfordQuadruped.git

$cd StanfordQuadruped
###请注意这一步如果出现安装下载失败，请反复执行
$sudo bash install.sh

#校准舵机
$sudo systemctl stop robot

$cd StanfordQudruped

$sudo pigpiod
##执行校准程序，每个都要校准，当它要求您将链接移动到水平位置时，您可能想知道到底什么使链接变为水平。答案是对齐每个链接的关节中心。例如，将上链节与水平方向对齐时，您需要使伺服花键和将上链节与下链节连接的螺栓之间的线尽可能水平。
$python3 calibrate_servos.py

$sudo systemctl start robot

#检查状态
sudo systemctl status robot
