
# should not be here after gitOTA
# -------------------------------

# umain.py
# first attempt for gitOTA

from time import sleep_ms
from machine import Pin

def body():
    
    ledb = Pin(4, Pin.OUT)
    #ledg = Pin(19, Pin.OUT)
    
    print('LED is on...')
    ledb.on()
    sleep_ms(3000)
    
    print('LED is off!\n')
    ledb.off()
    sleep_ms(2500)
