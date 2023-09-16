import LCD_1in44
import os
import signal
import time
import subprocess
import logging
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.basicConfig(level=logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console_handler)

LCD = LCD_1in44.LCD()
LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT)

file = r'/var/ramdisk/cam.jpg'
# libcamera-still -k -t 0 --rawfull --nopreview --width 4624 --height 3472 --mode 4624:3472 -o 16mp.jpg
command = ['libcamera-still', '-s',  '-t', '30000', '--nopreview', '--autofocus-mode', 'auto', 
           '--width', '4624', '--height', '3472', '--mode', '4624:3472', '-o', file]
process = None
try:
    process = subprocess.Popen(command)
    while True:
        data = input("hit enter to process image")
        process.send_signal(signal.SIGUSR1)
        time.sleep(3)
        if os.path.isfile(file):
            print('file found')
            im = Image.open(file)
            new_width  = 128
            new_height = 128
            im1 = im.resize((new_width, new_height), Image.ANTIALIAS)
            time.sleep(1)
            LCD.LCD_ShowImage(im1,0,0)
except Exception as error:
    print("An exception occurred:", error)
    if process is not None:
        process.kill()

