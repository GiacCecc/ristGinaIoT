#
# Giacomo Ceccarelli
# Berlin, 11.05.2023
# v 0.2
# ---------------------------------------------------------

from time import ticks_ms
start_time = ticks_ms()

from machine import Pin
from time import sleep_ms

import onewire, ds18x20

from utils.secrets import MONGO_SRC, WHAT_PHONE_NR, WHAT_API_KEY
from utils.settings import TEMP_MAX, MAX_NLOGS_NIR, MSG_TIMEDELTA

import libs.uutil as util
import libs.uwhat as what
import libs.umongo as mongo
import libs.ugit as ugit


def check_update(pprint=False):
    OTA_TRIGGER = mongo.get_OTA_TRIGGER(pprint=pprint)
    print('\n-------------------------------------------\n')
    print(f'OTA_TRIGGER is set to {OTA_TRIGGER} ---+ ', end='')

    if OTA_TRIGGER:
        print('It´s time to UPDATE Over The Air (OTA)...\n')
        sleep_ms(2000)
        mongo.update_OTA_TRIGGER(value=False, pprint=pprint)
        mongo.insert_update(pprint=pprint)
        ugit.pull_all(isconnected=True)
    else:
        print('NO UPDATE NOW +-\n')
        sleep_ms(1000)
    
def body(pprint=False):
    #i = 1/0
    
    # Instatiate DS18B20
    # -------------------------------------------------------------------
    ds = ds18x20.DS18X20(onewire.OneWire(Pin(22)))
    roms = ds.scan()
    
    ds.convert_temp()
    sleep_ms(2000)
    
    temp = ds.read_temp(roms[0])
    print('Temperature (DS18B20): {:.2f} °C'.format(temp))
    mongo.insert_temp(temp, pprint=pprint)
    print('-Temperature inserted into MongoDB')
    
    # --------------- CHECK LOGS AND SEND WHATMSG IF WHATMSG_CONDS
    if temp >= TEMP_MAX:
        print('--Temperature ≥ {}'.format(TEMP_MAX))
        temps = mongo.last_nlogs(MONGO_SRC.Collections.logs,
                                 MAX_NLOGS_NIR,
                                 'temp',
                                 pprint=pprint)
        
        if all([i >= TEMP_MAX for i in temps]):
            print('---All last {} temperatures ≥ {}'.format(MAX_NLOGS_NIR, TEMP_MAX))
            timedelta = what.timedelta_last()
            
            if timedelta >= MSG_TIMEDELTA:
                print('---Timedelta from last whatmsg: {} ≥ {}'.format(timedelta, MSG_TIMEDELTA))
                msg = 'ALLARME! Temperatura CF01: {:.2f}'.format(temp)
                what.sendmsg(WHAT_PHONE_NR,
                             WHAT_API_KEY,
                             util.url_encode(msg),
                             pprint=pprint)
                print('-- whatmsg sent...')
                mongo.insert_msg(msg, pprint=pprint)
                print('- whatmsg inserted into MongoDB\n')

def report_error(err, wlan, pprint=False):
    tb_str = util.get_traceback_string(err)
    print(tb_str, '\n')
    
    if 'wlan' in locals():
        if wlan.station.isconnected():
            mongo.insert_error(tb_str, pprint=pprint)
            print('-ERROR inserted into MongoDB\n')
