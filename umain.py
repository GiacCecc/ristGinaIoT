
# should be here after gitOTA
# ---------------------------

# umain.py
# first attempt for gitOTA

from time import sleep_ms
from machine import Pin

def blinkk(led):
    for i in range(3):
        led.on()
        sleep_ms(500)
        led.off()
        sleep_ms(500)
        
def body():
    
    ledb = Pin(4, Pin.OUT)
    ledg = Pin(19, Pin.OUT)
    
    ledb.on()
    ledg.on()
    sleep_ms(3000)
    ledb.off()
    ledg.off()
    sleep_ms(3000)
    
    
    print('BLUE is blinking...')
    blinkk(ledb)
    
    print('GREEN is blinking...')
    blinkk(ledg)
