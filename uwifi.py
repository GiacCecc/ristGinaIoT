# WifiConnection
# Implement a Class to simplify WiFi connection management
# ------------------------------------------------------------------------
#
# Giacomo Ceccarelli
# Berlin, 18.04.2023

from time import sleep_ms
from machine import Pin

import network
import socket

from uutil import blink_if

class WifiConnection():
    
    def __init__(self, ssid, password, ledPin):
        self.ssid = ssid
        self.password = password
        self.station = network.WLAN(network.STA_IF)
        self.led = Pin(ledPin, Pin.OUT)

    def connect(self):
        self.station.active(True)
        
        if self.station.isconnected():
            return None
        
        print('Trying to connect to %s...' % self.ssid)
        self.station.connect(self.ssid, self.password)
        
        for retry in range(200):
            connected = self.station.isconnected()
            if connected:
                break
            sleep_ms(100)
            print('.', end='')
        
        if connected:
            print('\nConnected. Network config: ', self.station.ifconfig())
        else:
            print('\nFailed. Not Connected to: ' + self.ssid)
        
        self.check_socket()
        sleep_ms(1000)
        blink_if(connected, led=self.led, nblink=3, timedelta=500, keep_on=True)
        print('')
        sleep_ms(1000)
        
        return connected
    
    def check_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 80))
            s.listen(5)
        except OSError as e:
            reset()
    
    def disconnect(self):
        self.station.disconnect()
        self.station.active(False)
        if self.led.value() == 1:
            self.led.value(0)
        print('Disconnected!\n')
    
    
