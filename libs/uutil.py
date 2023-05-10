
import ure
from machine import Pin
from time import sleep_ms

# ------------------------------------------------------------------------

def url_encode(input_string):
    
    encoded_string = ""
    
    for char in input_string:
        
        if ure.match("^[a-zA-Z0-9_.!~*'()-]$", char):
            encoded_string += char
        else:
            encoded_string += '%' + '{:02x}'.format(ord(char)).upper()
            
    return encoded_string

#input_string = 'Temperature: 18.6875, last WhatsApp sent 78049 seconds ago.'
#print(url_encode(input_string))


def url_decode(url_encoded_string):
    
    decoded_string = ""
    
    i = 0
    while i < len(url_encoded_string):
        
        if url_encoded_string[i] == '%':
            decoded_string += chr(int(url_encoded_string[i+1:i+3], 16))
            i += 3
        else:
            decoded_string += url_encoded_string[i]
            i += 1
            
    return decoded_string

"""
# Define the URL encoded string
url_encoded_string = "Temperature%3A%2018.5%2C%20last%20WhatsApp%20sent%20179474%20seconds%20ago."
# Call the url_decode() function and print the result
decoded_string = url_decode(url_encoded_string)
print(decoded_string)
"""

# ------------------------------------------------------------------------

def get_datetime_tuple(dt_str): # TODO::: check time format name and standards
    
    YY = dt_str[:4]
    MM = dt_str[5:7]
    DD = dt_str[8:10]
    hh = dt_str[11:13]
    mm = dt_str[14:16]
    ss = dt_str[17:19]
    
    return (int(YY), int(MM), int(DD), int(hh), int(mm), int(ss), 0, 0)

# ------------------------------------------------------------------------

def print_response_info(response):
    
    if response == None:
        raise TypeError('Argument fro print_response_info must be a HTTP response from urequest')
    
    print('Response to {}:'.format('<TODO: MongoDB Data API URL Endpoint>'))
    print('----------------------------------------------------------------')
    print('status_code:        ', response.status_code)
    print('reason:             ', response.reason)
    print('content:            ', response.content)
    print('text:               ', response.text)
    print('')

# ------------------------------------------------------------------------

def blink_if(condition, led=Pin(2, Pin.OUT), nblink=3, timedelta=500, keep_on=True):
    
    if condition:
        for i in range(nblink):
            led.value(1)
            sleep_ms(500)
            if (i != nblink-1) or ((i == nblink-1) and (not keep_on)):
                led.value(0)
                sleep_ms(500)
    else:
        pass

#def led_off(led=Pin(2, Pin.OUT)):
#    led.off()


