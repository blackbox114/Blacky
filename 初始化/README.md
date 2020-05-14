# 树莓派初始化
### 修改wifi配置
请在*Blacky\初始化\appliance\etc\wpa_supplicant*中添加自己的wifiSSID和PSWD，具体格式参考：

ssid：LBm

pswd：11111111

```text
network={
        ssid="LBm"
        psk="11111111"
}
```


### 覆盖文件
烧录镜像完成后，请直接将本仓库复制粘贴到boot文件夹，覆盖重复的文件。

### 启动和ssh

正常上电启动。请提供稳定网络进行初始化，初始化需要一些时间，初次初始化可以外界屏幕和键盘观察进度。ok后可直接ssh进入。请按照提示修改密码和ip

### 进入写模式

rw

### 换源
```shell
$sudo sed -i 's|raspbian.raspberrypi.org|mirrors.ustc.edu.cn/raspbian|g' /etc/apt/sources.list

$sudo sed -i 's|//archive.raspberrypi.org|//mirrors.ustc.edu.cn/archive.raspberrypi.org|g' /etc/apt/sources.list.d/raspi.list

$sudo apt-get update
```
### pqi更新pip源
```shell
$pip install pqi

$pqi

$pqi use ustc
```
### 自动对时
```shell
$sudo date  --s="2020-11-08 20:42:00"

$sudo apt-get install ntpdate 
```
### 更换为国内对时服务器
```shell
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
```
### 下载项目文件
```shell
$git clone https://github.com/stanfordroboticsclub/StanfordQuadruped.git

$cd StanfordQuadruped
```
### 请注意这一步如果出现安装下载失败，请反复执行
```shell
$sudo bash install.sh
```
### 校准舵机
```shell
$sudo systemctl stop robot

$cd StanfordQudruped

$sudo pigpiod
```
#### 执行校准程序，每个都要校准，当它要求您将链接移动到水平位置时，您可能想知道到底什么使链接变为水平。答案是对齐每个链接的关节中心。例如，将上链节与水平方向对齐时，您需要使伺服花键和将上链节与下链节连接的螺栓之间的线尽可能水平。
```shell
$python3 calibrate_servos.py

$sudo systemctl start robot
```
### 检查状态
```shell
$sudo systemctl status robot
```
