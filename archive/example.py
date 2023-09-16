from picamera2 import Picamera2
import time
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start(show_preview=False)
time.sleep(1)
img = picam2.switch_mode_and_capture_file(capture_config, "test.jpg")
picam2.close()