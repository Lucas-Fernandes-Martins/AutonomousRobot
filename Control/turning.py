from arduino_interface import ArduinoInterface
import time

class Turning:


    def __init__(self, arduino_interface: ArduinoInterface):
        self.arduino_interface = arduino_interface

    def turn_90_left(self):
        time.sleep(0.2)
        self.arduino_interface.set_wheel_right()
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)


    def turn_90_right(self):
        time.sleep(0.2)
        self.arduino_interface.set_wheel_left()
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)

    def turn_180(self):
        self.arduino_interface.set_wheel_velocity(100, 0)
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)
