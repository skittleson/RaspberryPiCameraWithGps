`# libcamera-still -k -t 0 --rawfull --nopreview --width 4624 --height 3472 --mode 4624:3472 -o 16mp.jpg`


auto focus
[Raspberry Pi Camera Autofocus: Complete Guide (V1, V2 & HQ) (arducam.com)](https://www.arducam.com/raspberry-pi-camera/autofocus/)
[libcamera and libcamera-apps - Arducam Wiki](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Libcamera-User-Guide/#for-arducam-16mp64mp-autofocus-camera)




fastest way to take a pix: `sudo libcamera-jpeg -t1 --rotation 180 --width 128 --height 128 --rawfull 1 -o cam.jpg`

16mp - `libcamera-still -t 5000 --width 4624 --height 3472 --mode 4624:3472 -o 16mp.jpg`
16mp - `sudo libcamera-jpeg -t1 --rotation 180 --width 4624 --height 3472 --autofocus-mode continuous --rawfull 1 -o cam3.jpg `

16mp - `libcamera-still -t 5000 --width 4624 --height 3472 --autofocus-mode continuous --keypress --mode 4624:3472 -o 16mp.jpg`