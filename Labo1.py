import json
import signal
import sys
import time
import urllib
import psutil
import requests

# nire api_key -> LT4QN4UG9NFH6UXD

def ram_atera():

    # psutil liburutegia erabiliz, %RAM atera
    ram = psutil.virtual_memory()[2]
    print("RAM: %" + str(ram))
    return ram

def cpu_atera():

    # psutil liburutegia erabiliz, %CPU atera
    cpu = psutil.cpu_percent(interval=0.5)
    print("CPU: %" + str(cpu))
    return cpu

def handler(sig_num, frame):

    kanalahustea(kanalId)
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)

def kanalasortutadagoen():

    # List your channels, kanalen zerrenda itzuli
    # Kanala sortuta dagoen ala ez konprobatuko dugu
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': 'LT4QN4UG9NFH6UXD'}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    edukia = json.loads(erantzuna.content)

    # Edukiaren luzera 0 baino handiagoa bada, orduan kanala sortuta dago
    if len(edukia) > 0:
        emaitza = True
    else:
        # Kanala ez dago sortuta
        emaitza = False

    return emaitza

def kanalalortu():

    # Kanala lortuko dugu
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': 'LT4QN4UG9NFH6UXD'}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    edukia = json.loads(erantzuna.content)
    kanalId = edukia[0]['id']
    kanalApi = edukia[0]['api_keys'][0]['api_key']
    return kanalId, kanalApi

def channelsortu():

    # Kanala sortu behar dugu
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'LT4QN4UG9NFH6UXD', 'name': 'KanalaLabo1', 'field1': "%CPU", 'field2': "%RAM"}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    edukia = json.loads(erantzuna.content)

def datuigoera(kanalApi):

    # Datuak igoko ditugu
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': kanalApi, 'field1': cpu_atera(), 'field2': ram_atera()}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

def kanalahustea(kanalId):

    # Kanala hustu egingo dugu, horretarako metodoa DELETE da
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/" + str(kanalId) + "/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia = {'api_key': 'LT4QN4UG9NFH6UXD'}
    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

if __name__ == '__main__':

    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')

    emaitza = kanalasortutadagoen()
    print("Kanala sortuta dago: " + str(emaitza))

    if not emaitza:
        # Kanala sortu behar da
        channelsortu()

    # Kanala badakigu sortuta dagoela, orain lortu egingo dugu
    kanalId, kanalApi = kanalalortu()

    while True:

        # Kanala sortuta dago, datuak igoko ditugu
        datuigoera(kanalApi)

        # 15 segunduro igoko ditu datuak
        time.sleep(15)
