# 导入库
from drv8833 import DRV8833
from time import time

# 初始化类
mt = DRV8833([(4,5),(2,3)], 10)

# 开始A控制
mt.start_a()

# 0~100 平均比例划分65535
mt.a_speed(10)

# 用原来的的PWM.duty_u16控制
mt.b_speed_u16(32767)

# 获取0-100划分的速度值
speed_a = mt.a_speed()
# 获取pwm的duty_u16划分的速度值
speed_b = mt.a_speed_u16()

# 显示速度
print(speed_a)
print(speed_b)

# a反转
mt.a_reverse()

# 停止A控制
mt.stop_a()

# 停止所有
mt.stop()