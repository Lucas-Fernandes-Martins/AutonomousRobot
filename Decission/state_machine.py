

class StateMachine:

    def __init__(self):
        """
        0 -> WAITING MISSION PLANNER
        1 -> FOLLOWING LINE
        2 -> AVOIDING OBSTACLE
        3 -> PERFORMING MISSION ACTION
        4 -> LOSS MODE
        """
        self.STATE = 0

    def return_state(self):
        return self.STATE

    def decide_state(self, corner, obstacle):
        if obstacle:
            self.STATE = 2
        elif corner:
            self.STATE = 0



