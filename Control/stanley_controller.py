from math import atan

class StanleyController:

    def __init__(self):
        self.k_cross_track_error = 1

    def get_error(self, point_to_be_followed):
        return self.k_cross_track_error*point_to_be_followed[0]  # + atan(x/y)
