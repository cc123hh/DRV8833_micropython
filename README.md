# DRV8833_micropython
## Introduction
Simple application of DRV8833 module may have problems writing module classes for the first time.
![DRV8833_module](./images/drv8833.jpg)

# How to use

Here's a simple example:
```
# Import library
from drv8833 import DRV8833

# Initialization class, parameters are [motor A, motor B] pin, STBY pin,pwm frequency
Here a,b are (4,5) and (2,3).
mt = DRV8833([(4,5),(2,3)], 10,20_000)

# start(motor_index)
# Start two motor controls
mt.start()

# speed(motor_index, speed)
# Speed range -100 ~ 100
Mt. Speed (0, 50)

# speed_u16(motor_index, speed)
# Use the original PWM.duty_u16 control
Mt. Speed_u16 (1327 67).

# Get the speed value for the 0-100 partition
speed_a = mt.speed()
# Get the speed value of the duty_u16 partition of pwm
speed_b = mt.speed_u16()

# Display speed
print(speed_a)
print(speed_b)

# a reversal
mt.reverse(0)

# Stop A control
mt.stop(0)

# Stop all
mt.stop()
```
# Fixed issues
STBY fixes that simplify the use of some methods: for example, 'speed(0,100)=speed_A(100)'
# Some unanswered questions
The code seems a little redundant and jumbled