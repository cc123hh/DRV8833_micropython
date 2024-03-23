from machine import Pin,PWM,UART
from drv8833 import DRV8833

mt = DRV8833([(4,5),(2,3)], 10)

# 0~100 平均比例划分65535
mt.a_speed(10)

# 用精准的pwm的duty_u16控制
mt.b_speed_u16(32767)


# 获取0-100划分的速度
speed_a = mt.a_speed()
# 获取pwm的duty_u16划分的速度
speed_b = mt.a_speed_u16()

print(speed_a)
print(speed_b)

# a反转
mt.a_reverse()

# 停止
mt.stop()