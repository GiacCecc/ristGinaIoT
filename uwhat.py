
import urequests as requests
from time import mktime

from uutil import get_datetime_tuple, print_response_info
import umongo as mongo
from secrets import MONGO_SRC


def timedelta_last():
    datetime_str_whatmsg = mongo.last_log(MONGO_SRC.Collections.messages, 'msgTime')
    datetime_str_temp = mongo.last_log(MONGO_SRC.Collections.logs, 'logTime')
    
    #print('datetime_str_whatmsg   :   ', datetime_str_whatmsg, type(datetime_str_whatmsg))
    #print('datetime_str_temp      :   ', datetime_str_temp, type(datetime_str_temp), '\n')
    
    epoch_whatmsg = mktime(get_datetime_tuple(datetime_str_whatmsg))
    epoch_temp    = mktime(get_datetime_tuple(datetime_str_temp))
    timedelta = epoch_temp - epoch_whatmsg
    #print(timedelta)
    
    return  timedelta

def sendmsg(phone_number, api_key, message, pprint=False):
    url = 'https://api.callmebot.com/whatsapp.php?phone=' + phone_number + '&text='+message+'&apikey=' + api_key
    response = requests.get(url)
    if pprint:
        print_response_info(response)
    response.close()
