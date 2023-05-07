

# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)

import gc
gc.collect()


"""
# Connect to WiFi
# -------------------------------------------------------------------
from utils.secrets import WIFI_SSID, WIFI_PASSWORD
from libs.uwifi import WifiConnection
import libs.umongo as mongo
from time import sleep_ms

wlan = WifiConnection(WIFI_SSID, WIFI_PASSWORD, ledPin=2)
wlan.connect()

SETTINGS = mongo.get_SET(pprint=False)

TEMP_MAX = SETTINGS[0]
MAX_NLOGS_NIR = SETTINGS[1]
LOG_TIMEDELTA = SETTINGS[2]
MSG_TIMEDELTA = SETTINGS[3]

sleep_ms(1000)
wlan.disconnect()
sleep_ms(1000)
"""