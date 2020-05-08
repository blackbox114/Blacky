/*
根据BNO080库编写
 在400kHz I2C上需要大约1ms的时间来读取传感器的记录
 loop里面在进行循环
 硬件连接：
 将I2C引脚从BNO080的I2C连接到Teensy。用短的microUSB->USB电缆将Teensy连接到R树莓派。
库地址https://github.com/sparkfun/SparkFun_BNO080_Arduino_Library
*/

#include <Wire.h>

#include "SparkFun_BNO080_Arduino_Library.h"
BNO080 myIMU;

long last_print = micros();

void setup()
{
  Serial.begin(500000);
  Serial.println();
  Serial.println("BNO080 IMU 监测中");

  Wire.begin();
  if (myIMU.begin() == false)
  {
    Serial.println("没有在默认的I2C接口检测到BNO080 。请检查线路是否通畅");
    while (1);
  }
  Wire.setClock(400000); //把I2C速度拉到400kHz
  //最快反馈速度400Hz -> 大约2.5ms给书没跑传输一次值
  myIMU.enableRotationVector(10); //每10ms更新一次数据
  Serial.println(F("启用"));
  Serial.println(F("输出数据格式为  i, j, k, real, accuracy"));
}

void loop()
{
  if (myIMU.dataAvailable() == true)
  {
    float quatI = myIMU.getQuatI();
    float quatJ = myIMU.getQuatJ();
    float quatK = myIMU.getQuatK();
    float quatReal = myIMU.getQuatReal();
    Serial.print(quatReal, 4);
    Serial.print(F(","));
    Serial.print(quatI, 4);
    Serial.print(F(","));
    Serial.print(quatJ, 4);
    Serial.print(F(","));
    Serial.print(quatK, 4);
    Serial.println();
  }
}
