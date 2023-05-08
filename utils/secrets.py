


# Customer Info
CUSTOMER    = 'RistGina'
CUSTOMER_ID = '0000'
DEVICE_ID   = f'{CUSTOMER_ID}-ESP32-GC01'



# WiFi - network credentials
### Danja
WIFI_SSID     = "Vodafone-F344"
WIFI_PASSWORD = "AhRdJCQmqmGaT7tN"
### RistGina/Giuseppe
# WIFI_SSID     = "FRITZ!Box 7530 TC"
# WIFI_PASSWORD = "35114311079506609844"



# MongoDB - Data API
MONGO_APP_ID  = 'data-trrur'
MONGO_API_KEY = '5xJNUtYIBJkQ8GXCmtA1OTMzfOpOy08PE5Be1ANrG4zexfwatiPJOTCpAWV3Kihm'

class mongoSource():
    dataSource = 'Cluster0'
    database   = 'CF01'
    
    class Collections():
        configSet = 'configSet'
        errors    = 'errors'
        logs      = 'logs'
        messages  = 'messages'
        reports   = 'reports'

MONGO_SRC = mongoSource()



# WhatsApp - CallMeBot credentials
### Giacomo
WHAT_PHONE_NR = '+4917644281013'
WHAT_API_KEY  = '5037297'
### RistGina/Giuseppe
# WHAT_PHONE_NR = '+393282890049'
# WHAT_API_KEY  = '2484013'

# GitHub Repository
# Repository must be public if no personal access token is supplied
GITHUB_USER  = 'GiacCecc'
GITHUB_REPO  = 'ristGinaIoT'
GITHUB_TOKEN = ''