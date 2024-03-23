# DRV8833_micropython
## Introduction
Simple application of DRV8833 module may have problems writing module classes for the first time.
![DRV8833_module](./images/drv8833.jpg)

# How to use

Here's a simple example:
```
# Import library
from drv8833 import DRV8833
from time import time

# Initialize the class
mt = DRV8833([(4,5),(2,3)], 10)

# Start A control
mt.start_a()

# 0 to 100 Average ratio partition 65535
mt.a_speed(10)

# Use the original PWM.duty_u16 control
mt.b_speed_u16(32767)

# Get the speed value for the 0-100 partition
speed_a = mt.a_speed()
# Get the speed value of the duty_u16 partition of pwm
speed_b = mt.a_speed_u16()

# Display speed
print(speed_a)
print(speed_b)

# a reversal
mt.a_reverse()

# Stop A control
mt.stop_a()

# Stop all
mt.stop()
```
# Some unanswered questions
There is no strong setting for STBY (because STBY can be directly connected to the positive electrode) : Automatically changing the value will enable STBY, and you can change it yourself if necessary. I didn't have this need to consider