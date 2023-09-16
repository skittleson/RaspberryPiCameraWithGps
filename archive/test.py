# https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/
import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.NULL)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)

picam2.start()
time.sleep(1)

picam2.set_controls( {"AfMode": 2 ,"AfTrigger": 0})
metadata = picam2.capture_file("focus.jpg")
# If your libcamera-dev version is 0.0.10, use the following code.
# AfMode Set the AF mode (manual, auto, continuous)
# For example, single focus: picam2.set_controls({"AfMode": 1 ,"AfTrigger": 0})
#              continuous focus: picam2.set_controls({"AfMode": 2 ,"AfTrigger": 0})

time.sleep(5)