import serial
import pynmea2

class Gps:
    """Get GPS data on demand"""

    # https://raspberrypi.stackexchange.com/questions/139894/is-this-an-acceptable-way-to-set-the-rx-tx-pins-for-uart1
    # https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/

    def __init__(self, port, baud= 9600):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=1.0)
        self.ser.open()
    
    def __del__(self):
        if self.ser is not None:
            if self.ser.is_open:
                self.ser.close()
            self.ser = None

    def get(self):
        new_data = self.ser.readline().decode("utf-8")
        if new_data[0:6] == "$GPRMC":
            gprmc = pynmea2.parse(new_data)
            return {'timestamp': gprmc.datetime, 'latitude': gprmc.latitude, 'longitude': gprmc.longitude}