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