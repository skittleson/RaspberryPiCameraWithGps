#  DIY Camera with Raspberry Pi and GPS

Project Goal: Create a compact, high-performance camera using Raspberry Pi, a camera module, and GPS for exceptional photography.

- [x] click up/down to preview images
- [x] Get some basic code in place.
- [x] click middle to delete it
- [ ] gps data
- [ ] add metadata to image
- [ ] speaker on image snap
- [ ] case
- [ ] battery

## Pre

To display pics [1.44inch LCD HAT - Waveshare Wiki](https://www.waveshare.com/wiki/1.44inch_LCD_HAT)
To install Arudcam [Quick Start - Arducam Wiki](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Quick-Start-Guide/)
[Troubleshooting - Arducam Wiki](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Troubleshooting/) - Cannot Allocate Memory  ha to be done


```
nano /boot/config.txt

camera_auto_detect=0
dtoverlay=vc4-kms-v3d,cma-128
dtoverlay=imx519
over_voltage=6

raspi-config
advance > glamor graphic accel > enable

sudo nano /boot/cmdline.txt
Add to the end: alloc_in_cma_threshold=16
sudo reboot now
```


fastest way to take a pix: `sudo libcamera-jpeg -t1 --rotation 180 --width 128 --height 128 --rawfull 1 -o cam.jpg`


## Getting Started

