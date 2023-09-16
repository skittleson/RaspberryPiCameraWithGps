import LCD_1in44
import LCD_Config
from PIL import Image
from time import strftime, localtime, sleep
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO

# key bindings
KEY_UP_PIN     = 6
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up


## camera
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (128, 128)})
picam2.configure(preview_config)
picam2.start_preview(Preview.NULL)
picam2.start()
sleep(2)

# Setup the LCD
LCD = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)
LCD.LCD_Clear()

while True:
	if GPIO.input(KEY1_PIN) == 0:
		print("take pix")
		new_file_name = strftime('%Y%m%d_%H%M%S', localtime(ti_m))
		metadata = picam2.capture_file("/tmp/cam.jpg")
		print(metadata)
		image = Image.open('/tmp/cam.jpg')
		sleep(1)
		LCD.LCD_ShowImage(image,0,0)

	if GPIO.input(KEY_UP_PIN) == 0:
		print("Up")
	if GPIO.input(KEY_LEFT_PIN) == 0:
		print("left")
		break

picam2.close()

