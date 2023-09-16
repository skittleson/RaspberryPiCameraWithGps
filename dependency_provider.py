import os
import LCD_1in44
from PIL import Image, ImageDraw
from time import strftime, localtime, sleep
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import time
import atexit
import logging
import threading
import datetime
from pprint import pprint


# key bindings
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16
KEY_BINDINGS = [KEY_UP_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN,
                KEY_RIGHT_PIN, KEY_PRESS_PIN, KEY1_PIN, KEY2_PIN, KEY3_PIN]

# multi image capture for better quality https://github.com/raspberrypi/picamera2/blob/main/examples/capture_average.py
# ram disk is required to keep this fast https://www.rickmakes.com/setting-up-a-ram-disk-on-a-raspberry-pi-4/


class DependencyProvider:
    IMAGES_PATH = '/home/support/campi/'

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup the LCD
        self.LCD = LCD_1in44.LCD()
        self.LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT)
        self.__lcd_text('loading', None)
        self.camera_start()
        atexit.register(self.dispose)

    def get_images(self) -> list[str]:
        """Get a list of images starting with the newest one"""

        paths = os.listdir(self.IMAGES_PATH)
        files = []
        for path in paths:
            if os.path.isfile(os.path.join(self.IMAGES_PATH, path)):
                files.append(path)
        files.reverse()
        return files
    
    def delete_image(self, image_path: str) -> None:
        os.remove(image_path)

    def display_image(self, image_path: str) -> None:
        im = Image.open(os.path.join(self.IMAGES_PATH, image_path))
        resized = im.resize(size=(128, 128))

        # storing thumbnails might be required before this.
        self.__lcd_text(None, resized)

    def __lcd_text(self, text: str, image: Image):
        # self.LCD.LCD_Clear()
        if text is None:
            self.LCD.LCD_ShowImage(image, 0, 0)
            return
        start_img = image
        if image is None:
            start_img = Image.new(mode="RGB", size=(128, 128))
        width, height = start_img.size
        draw = ImageDraw.Draw(start_img)
        textwidth, textheight = draw.textsize(text)
        margin = 2
        x = width - textwidth - margin
        y = height - textheight - margin
        draw.text((x, y), text)
        self.LCD.LCD_ShowImage(start_img, 0, 0)

    def diag():
        picam2 = Picamera2()
        pprint(Picamera2.global_camera_info())
        pprint(picam2.sensor_modes)
        picam2 = None

    def dispose(self):
        logging.info("Cleaning up")
        self.__lcd_text('DONE', None)
        self.camera_close()

    def lcd_input(self) -> int:
        """
        Selected input on LCD screen.

        :return: int of pulled up GPIO. When zero, nothing has occurred
        """
        for key in KEY_BINDINGS:
            if GPIO.input(key) == 0:
                return key
        return 0

    def focus(self):
        self.cam_hardware.set_controls({"AfMode": 1, "AfTrigger": 0})
        self.__lcd_text('focusing', self.current_preview_img)
        time.sleep(0.5)

    def camera_start(self) -> None:
        self.cam_hardware = Picamera2()
        self.preview_config = self.cam_hardware.create_preview_configuration(
            main={"size": (128, 128)})
        self.cam_hardware.configure(self.preview_config)
        self.cam_hardware.start_preview(Preview.NULL)
        self.cam_hardware.start()
        time.sleep(1)
        # https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/PiCamera2-User-Guide/#:~:text=hawkeye%2D64mp-,PiCamera2%20Focus%20Controller%20Instruction,-Step%201.%20Ensure
        self.cam_hardware.set_controls({"AfMode": 1, "AfTrigger": 0})

    def camera_close(self) -> None:
        if self.cam_hardware is not None:
            self.cam_hardware.close()
            self.cam_hardware = None

    def _file_transfer(self, source_image_array, destination_file):
        def file_transfer(threadsource_image_array, thread_destination_file):
            logging.info(f'start saving {thread_destination_file}')
            Image.fromarray(threadsource_image_array).rotate(
                90).save(thread_destination_file)
            logging.info(f'end saving {thread_destination_file}')

        # Create a new thread for file transfer
        transfer_thread = threading.Thread(
            target=file_transfer, args=(source_image_array, destination_file))
        transfer_thread.start()

    def camera_preview_loop(self) -> None:
        """
        applies current image in camera preview to LCD screen

        Returns:
            None: This method returns nothing but an LCD screen update will occur.

        Raises:
            LookupError: Camera was not started.
        """
        if self.cam_hardware is None:
            raise LookupError("Must start camera")
        self.__lcd_text(None, self.__preview_image(
            self.cam_hardware.capture_array()))

    def __preview_image(self, data: object) -> Image:
        self.current_preview_img = Image.fromarray(data).rotate(90)
        return self.current_preview_img

    def camera_snap(self) -> bool:
        """
        Take then save a picture with camera

        Args:
            path (str): It can be any valid string path.

        Returns:
            bool: This method returns True if the task is successful,
                otherwise False.

        Raises:
            ValueError: If path is not a string.
            ValueError: If path is not a directory.
            LookupError: Camera was not started.
        """
        if self.cam_hardware is None:
            raise LookupError("Must start camera")
        logging.info('taking better photo')
        config = self.cam_hardware.create_still_configuration(
            main={"size": (3840, 2160)})
        # (1920, 1080)
        # (2328, 1748)
        # (3840, 2160)
        # (4656, 3496)
        self.__lcd_text('capturing', self.current_preview_img)
        captured_array = self.cam_hardware.switch_mode_and_capture_array(
            config)

        # offload saving the image right away
        new_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self._file_transfer(
            captured_array, fr'{self.IMAGES_PATH}{new_file_name}.jpg')
        preview_image = self.cam_hardware.switch_mode_and_capture_array(
            self.preview_config)
        self.__lcd_text('complete', self.__preview_image(preview_image))
        time.sleep(2)
        # self.__lcd_temp_text = (datetime.datetime.now(), 'complete')
        return True
