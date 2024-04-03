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
    __direction_a = True
    __direction_b = True
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

    def start(e):
        if e.__stby:
            e.setSTBY(1)
        e.start_A()
        e.start_B()

    def start_A(e):
        if e.__stby:
            e.setSTBY(1)
        if e.__direction_a:
            e.__ain1.duty_u16(e._max)
            e.__ain2.duty_u16(e.a_duty_u16)
        else:
            e.__ain2.duty_u16(e._max)
            e.__ain1.duty_u16(e.a_duty_u16)

    def start_B(e):
        if e.__stby:
            e.setSTBY(1)
        if e.__direction_b:
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
        e.__bin1.duty_u16(e._max)
        e.__bin2.duty_u16(e._max)

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

    def reverse(e, code):
        if code == 0:
            e.reverse_A()
        elif code == 1:
            e.reverse_B()
        else:
            raise Exception("No this motor")

    def reverse_A(e):
        e.__direction_a = not e.__direction_a
        e.start_A()

    def reverse_B(e):
        e.__direction_b = not e.__direction_b
        e.start_B()

    def __calc_speed(e, speed):
        return int(((100 - speed) / 100) * 65535)

    def direction(e, motor_index, dirction):
        if motor_index == 0:
            return e.direction_A(dirction)
        elif motor_index == 1:
            return e.direction_B(dirction)
        else:
            raise Exception("No this motor")

    def direction_A(e, direction: bool = None):
        e.__direction_a = bool(direction)
        return e.__direction_a

    def direction_B(e, direction: bool = None):
        e.__direction_b = bool(direction)
        return e.__direction_b

    def speed(e, code, s):
        if code == 0:
            return e.speed_A(s)
        elif code == 1:
            return e.speed_B(s)
        else:
            raise Exception("No this motor")

    def speed_A(e, speed: int = None):

        if speed != None:
            if speed > 100:
                raise SpeedOverRangeError(f"Speed too big, range:0-100. speed:{speed}")
            elif speed < 0:
                raise SpeedOverRangeError(
                    f"Speed too small, range:0-100. speed:{speed}"
                )

            e.a_duty_u16 = e.__calc_speed(speed)
            e.start_A()
            return speed
        else:
            return int(100 - 100 * (e.a_duty_u16 / e._max))

    def speed_B(e, speed: int = None):

        if speed != None:
            if speed > 100:
                raise SpeedOverRangeError(f"Speed too big, range:0-100. speed:{speed}")
            elif speed < 0:
                raise SpeedOverRangeError(
                    f"Speed too small, range:0-100. speed:{speed}"
                )

            e.b_duty_u16 = e.__calc_speed(speed)
            e.start_B()
            return speed
        else:
            return int(100 - 100 * (e.a_duty_u16 / e._max))

