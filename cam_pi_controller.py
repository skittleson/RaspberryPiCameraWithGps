import dependency_provider
import logging

logging.basicConfig(level=logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger('').addHandler(console_handler)

if __name__ == '__main__':
    controller = dependency_provider.DependencyProvider()
    logging.info("v38")
    try:
        gallery_mode = False
        gallery_image_index = -1
        while True:
            lcd_key = controller.lcd_input()
            if gallery_mode:
                if gallery_image_index == -1:
                    gallery_image_index = 0
                    controller.display_image(controller.get_images()[
                                             gallery_image_index])

                elif lcd_key == dependency_provider.KEY_PRESS_PIN:
                    controller.delete_image(controller.get_images()[
                        gallery_image_index])
                    gallery_image_index = 0

                # UP and DOWN keys scoll through images
                elif lcd_key == dependency_provider.KEY_UP_PIN or lcd_key == dependency_provider.KEY_DOWN_PIN:
                    images = controller.get_images()
                    if lcd_key == dependency_provider.KEY_UP_PIN:
                        gallery_image_index = gallery_image_index - 1
                        if gallery_image_index < 0:
                            gallery_image_index = (len(images)-1)
                    elif lcd_key == dependency_provider.KEY_DOWN_PIN:
                        gallery_image_index = gallery_image_index + 1
                        if gallery_image_index > (len(images)-1):
                            gallery_image_index = 0
                    controller.display_image(controller.get_images()[
                                             gallery_image_index])
                elif lcd_key == dependency_provider.KEY_LEFT_PIN or lcd_key == dependency_provider.KEY_RIGHT_PIN:
                    gallery_mode = not gallery_mode
                    controller.camera_start()
            else:
                controller.camera_preview_loop()
                if lcd_key == dependency_provider.KEY_PRESS_PIN:
                    controller.camera_snap()
                elif lcd_key == dependency_provider.KEY1_PIN:
                    controller.focus()
                elif lcd_key == dependency_provider.KEY2_PIN:
                    controller.focus()
                elif lcd_key == dependency_provider.KEY3_PIN:
                    controller.dispose()
                    break
                elif lcd_key == dependency_provider.KEY_LEFT_PIN or lcd_key == dependency_provider.KEY_RIGHT_PIN:
                    gallery_mode = not gallery_mode
                    gallery_image_index = -1
                    controller.camera_close()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        controller.dispose()
