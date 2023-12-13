import cv2
from picamera.array import PiRGBArray
import picamera

class Camera:

    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (int(1920/4), int(1088/4))
        self.camera.framerate = 80

        self.camera.start_recording('testRecording.h264')

        self.cap=picamera.array.PiRGBArray(self.camera, size = (int(1920/4),int(1088/4) ))

    def get_image(self):
        self.camera.capture(self.cap, use_video_port=True, resize = (int(1920/4),int(1088/4)), format="bgr")
        img=self.cap.array
        self.cap.truncate(0)
        return img
