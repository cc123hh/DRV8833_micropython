from machine import PWM, Pin


class SpeedOverRangeError(Exception):
    def __init__(self, message):
        self.message = message


class DRV8833:
    # Pins
    __ain1: PWM = None
    __ain2: PWM = None
    __bin1: PWM = None
    __bin2: PWM = None
    __stby: Pin = None

    # States
    direction_a = True
    direction_b = True
    a_duty_u16 = 65535
    b_duty_u16 = 65535

    # protect
    _max = 65535

    def __init__(e, ab_pins: tuple, stby_pin: int = None, frequency: int = 20_000):

        e.__ain1 = PWM(Pin(ab_pins[0][0], Pin.OUT), freq=frequency)
        e.__ain2 = PWM(Pin(ab_pins[0][1], Pin.OUT), freq=frequency)
        if len(ab_pins) > 1:
            e.__bin1 = PWM(Pin(ab_pins[1][0], Pin.OUT), freq=frequency)
            e.__bin2 = PWM(Pin(ab_pins[1][1], Pin.OUT), freq=frequency)

        if stby_pin != None:
            e.__stby = Pin(stby_pin, Pin.OUT)

    def setSTBY(e, state):
        e.__stby.value(bool(state))

    def start(e,motor_index=None):
        if e.__stby:
            e.setSTBY(1)

        if motor_index == 0:
            e.start_A()
        elif motor_index == 1:
            e.start_B()
        elif motor_index == None:
            e.start_A()
            e.start_B()
        else:
            raise Exception("No this motor")
        e.start_A()
        e.start_B()

    def start_A(e):
        if e.__stby:
            e.setSTBY(1)
        if e.direction_a:
            e.__ain1.duty_u16(e._max)
            e.__ain2.duty_u16(e.a_duty_u16)
        else:
            e.__ain2.duty_u16(e._max)
            e.__ain1.duty_u16(e.a_duty_u16)

    def start_B(e):
        if e.__stby:
            e.setSTBY(1)
        if e.__bin1 and e.__bin2:
            if e.direction_b:
                e.__bin1.duty_u16(e._max)
                e.__bin2.duty_u16(e.b_duty_u16)
            else:
                e.__bin2.duty_u16(e._max)
                e.__bin1.duty_u16(e.b_duty_u16)

    def stop(e):
        if e.__stby:
            e.setSTBY(0)
        e.stop_A()
        if e.__bin1:
            e.stop_B()

    def stop_A(e):
        e.__ain1.duty_u16(e._max)
        e.__ain2.duty_u16(e._max)

    def stop_B(e):
        if e.__bin1 and e.__bin2:
            e.__bin1.duty_u16(e._max)
            e.__bin2.duty_u16(e._max)
    
    def speed_u16(e, motor_index, speed):
        if motor_index == 0:
            return e.speed_A_u16(speed)
        elif motor_index == 1:
            return e.speed_B_u16(speed)
        elif motor_index == None:
            return (
                e.speed_A_u16(speed),
                e.speed_B_u16(speed),
            )
        else:
            raise Exception("No this motor")

    def speed_A_u16(e, speed: int = None):
        if speed != None:
            e.a_duty_u16 = speed
            e.start_A()
        else:
            return e.a_duty_u16

    def speed_B_u16(e, speed: int = None):
        if speed != None:
            e.b_duty_u16 = speed
            e.start_B()
        else:
            return e.b_duty_u16

    def reverse(e, motor_index=None):
        if motor_index == 0:
            e.reverse_A()
        elif motor_index == 1:
            e.reverse_B()
        elif motor_index == None:
            e.reverse_A()
            e.reverse_B()
        else:
            raise Exception("No this motor")

    def reverse_A(e):
        e.direction_a = not e.direction_a
        e.start_A()
        return e.direction_a

    def reverse_B(e):
        e.direction_b = not e.direction_b
        e.start_B()
        return e.direction_b

    def __calc_speed(e, speed):
        return int(((100 - speed) / 100) * 65535)

    def direction(e, motor_index, dirction=None):
        if motor_index == 0:
            return e.direction_A(dirction)
        elif motor_index == 1:
            return e.direction_B(dirction)
        elif motor_index == None:
            return (
                e.direction_A(dirction),
                e.direction_B(dirction),
            )
        else:
            raise Exception("No this motor")

    def direction_A(e, direction: bool = None):
        e.direction_a = bool(direction)
        return e.direction_a

    def direction_B(e, direction: bool = None):
        e.direction_b = bool(direction)
        return e.direction_b

    def speed(e, motor_index, s):
        if motor_index == 0:
            return e.speed_A(s)
        elif motor_index == 1:
            return e.speed_B(s)
        elif motor_index == None:
            return (
                e.speed_A(s),
                e.speed_B(s),
            )
        else:
            raise Exception("No this motor")

    def speed_A(e, speed: int = None):

        if speed != None:
            if speed > 100:
                raise SpeedOverRangeError(f"Speed too big, range:-100~100. Given speed:{speed}")
            elif speed < -100:
                raise SpeedOverRangeError(
                    f"Speed too small, range:-100~100. Given speed:{speed}"
                )

            e.a_duty_u16 = e.__calc_speed(speed)
            if(speed < 0):
                e.direction_A(False)
            else:
                e.direction_A(True)
            e.start_A()
            return speed
        else:
            return int(100 - 100 * (e.a_duty_u16 / e._max))

    def speed_B(e, speed: int = None):

        if speed != None:
            if speed > 100:
                raise SpeedOverRangeError(f"Speed too big, range:-100~100. Given Speed:{speed}")
            elif speed < 0:
                raise SpeedOverRangeError(
                    f"Speed too small, range:-100~100. Given Speed:{speed}"
                )

            e.b_duty_u16 = e.__calc_speed(speed)
            if(speed < 0):
                e.direction_B(False)
            else:
                e.direction_B(True)
            e.start_B()
            return speed
        else:
            return int(100 - 100 * (e.a_duty_u16 / e._max))

