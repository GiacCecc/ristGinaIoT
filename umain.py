
# should be here after gitOTA
# ---------------------------

# umain.py
# first attempt for gitOTA

from time import sleep_ms
from machine import Pin

def body():
    
    ledb = Pin(4, Pin.OUT)
    ledg = Pin(19, Pin.OUT)
    
    print('LEDs are on...')
    ledb.on()
    ledg.on()
    sleep_ms(3000)
    
    print('LEDs are off!\n')
    ledb.off()
    ledg.off()
    sleep_ms(2500)