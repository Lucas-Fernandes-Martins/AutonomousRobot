from arduino_interface import ArduinoInterface

class ObstacleDetection:

    def __init__(self, arduino_interface: ArduinoInterface):
        self.arduino_interface = arduino_interface

    def get_detected_obstacle(self):
        d = self.arduino_interface.get_dected_distance()
        if not d:
            return False
        return (d < 6 and d != 2 and d>0)
