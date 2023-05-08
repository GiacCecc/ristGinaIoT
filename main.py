#
# Giacomo Ceccarelli
# Berlin, 07.05.2023
# v 0.2
# ---------------------------------------------------------

from time import ticks_ms
start_time = ticks_ms()

from machine import Pin, RTC, deepsleep
from time import sleep_ms

import onewire, ds18x20
import uio, sys

from utils.secrets import WIFI_SSID, WIFI_PASSWORD, MONGO_SRC, WHAT_PHONE_NR, WHAT_API_KEY
from utils.settings import TEMP_MAX, MAX_NLOGS_NIR, LOG_TIMEDELTA, MSG_TIMEDELTA

import libs.uutil as util
import libs.uwhat as what
import libs.umongo as mongo
from libs.uwifi import WifiConnection

pprint = False #True # Print responses for mongoDB requests

# Instatiate DS18B20
# -------------------------------------------------------------------
ds = ds18x20.DS18X20(onewire.OneWire(Pin(22)))
roms = ds.scan()

# Connect to WiFi
# -------------------------------------------------------------------
wlan = WifiConnection(WIFI_SSID, WIFI_PASSWORD, ledPin=2)
wlan.connect()

try:
    #i = 1/0
    print('\n-------------------------------------------\n')
    OTA_TRIGGER = mongo.get_OTA_TRIGGER(pprint=pprint)
    print(f'OTA_TRIGGER is set to {OTA_TRIGGER} ---+ ', end='')
    if OTA_TRIGGER:
        print('It´s time to UPDATE Over The Air (OTA) +-\n')
        # ugit.update()
    else:
        print('NO UPDATE NOW +-\n')
        
    
    ds.convert_temp()
    sleep_ms(2000)
    
    temp = ds.read_temp(roms[0])
    print('Temperature (DS18B20): {:.2f} °C'.format(temp))
    mongo.insert_temp(temp, pprint=pprint)
    print('-Temperature inserted into MongoDB')
    
    # --------------- CHECK LOGS AND SEND WHATMSG IF WHATMSG_CONDS
    #TEMP_MAX = 13
    if temp >= TEMP_MAX:
        print('--Temperature ≥ {TEMP_MAX}')
        temps = mongo.last_nlogs(MONGO_SRC.Collections.logs,
                                 MAX_NLOGS_NIR,
                                 'temp',
                                 pprint=pprint)
        
        if all([i >= TEMP_MAX for i in temps]):
            print('---All last {MAX_NLOGS_NIR} temperatures ≥ {TEMP_MAX}')
            timedelta = what.timedelta_last()
            
            if timedelta >= MSG_TIMEDELTA:
                print('---Timedelta from last whatmsg: {timedelta} ≥ {MSG_TIMEDELTA}')
                msg = 'Temperature: {:.2f}, last WhatsApp sent {} sec. ago.'.format(temp, timedelta)
                what.sendmsg(WHAT_PHONE_NR,
                             WHAT_API_KEY,
                             util.url_encode(msg),
                             pprint=pprint)
                print('-- whatmsg sent...')
                mongo.insert_msg(msg, pprint=pprint)
                print('- whatmsg inserted into MongoDB\n')
    
except Exception as err:
    tb = uio.StringIO()
    sys.print_exception(err, tb)
    tb_str = tb.getvalue()
    mongo.insert_error(tb_str, pprint=pprint)
    print(tb_str, '\n')
    
finally:
    sleep_ms(500)
    wlan.disconnect()

sleep_ms(1000)
end_time = ticks_ms()

exec_time = end_time - start_time # execution time in ms
deepsleep_time = (LOG_TIMEDELTA * 1000) - exec_time - 690

#print("LOG_TIMEDELTA:  ", LOG_TIMEDELTA * 1000, "ms")
#print("time_taken:     ", time_taken, "ms")
#print("deepsleep_time: ", deepsleep_time, "ms")
print(f'--- deepsleep for {deepsleep_time} ms\n')
#sleep_ms(1000)




deepsleep(deepsleep_time) # LOG_TIMEDELTA - execTime