# DRV8833_micropython
## 简介
DRV8833 模块的简单应用，可能有问题，第一次写模块类。
![DRV8833模块](./images/drv8833.jpg)

# 如何使用

这是一个简单的例子：
```
# 导入库
from drv8833 import DRV8833

# 初始化类, 参数是[电机A,电机B]的引脚，STBY引脚,pwm频率
# 这里a,b是(4,5)和(2,3)
mt = DRV8833([(4,5),(2,3)], 10,20_000)

# start(motor_index)
# 开始两个电机控制
mt.start()

# speed(motor_index, speed)
# 速度范围 -100 ~ 100
mt.speed(0,50)

# speed_u16(motor_index, speed)
# 用原来的的PWM.duty_u16控制
mt.speed_u16(1,32767)

# 获取0-100划分的速度值
speed_a = mt.speed()
# 获取pwm的duty_u16划分的速度值
speed_b = mt.speed_u16()

# 显示速度
print(speed_a)
print(speed_b)

# a反转
mt.reverse(0)

# 停止A控制
mt.stop(0)

# 停止所有
mt.stop()
```
# 修复的问题
STBY修复，简化了一些方法的使用方法：例如`speed(0,100)=speed_A(100)`
# 一些没解决的问题
代码好像有点冗余混杂