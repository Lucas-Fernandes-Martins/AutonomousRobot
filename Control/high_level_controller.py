from arduino_interface import ArduinoInterface
from Control.turning import Turning
from Control.pid_control import PID
from Control.stanley_controller import StanleyController

class HighLevelController:

    def __init__(self, arduino_interface: ArduinoInterface):
        """
        action 0 -> follow line
        action 1 -> stop
        action 2 -> turn right 90 degrees
        action 3 -> turn left 90 degrees
        action 4 -> turn 180 degrees
        action 5 -> pass
        action 6 -> obstacle avoidance
                """
        self.arduino_interface = arduino_interface
        self.action = 0
        self.turning_action = Turning(self.arduino_interface)
        self.pid_control = PID()
        self.stanley_controller = StanleyController()
        self.error = 0



    def set_action(self, set_action):
        self.action = set_action



    def perform_action(self):
        if self.action == 0:
            w, v = self.pid_control.get_control_inputs(self.error)
            self.arduino_interface.set_wheel_velocity(w, v)
        elif self.action == 5:
            pass
        elif self.action == 4:
            self.turning_action.turn_180()
        elif self.action == 3:
            self.turning_action.turn_90_left()
        elif self.action == 2:
            self.turning_action.turn_90_right()
        elif self.action == 1:
            self.arduino_interface.stop()



    def update_error(self, point_to_be_followed):
        self.error = self.stanley_controller.get_error(point_to_be_followed)


