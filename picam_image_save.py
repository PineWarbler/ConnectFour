from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview() # will only appear on monitor directly connected to RPi
# Camera warm-up time
sleep(5)
camera.capture('test_image1.jpg')
camera.stop_preview()