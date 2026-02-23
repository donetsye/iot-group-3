# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network # library for wifi connection on esp32
import time

SSID = 'zhenchikk'
PASSWORD = 'blablabla'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print('.', end='')
    print('\nConnected!')
    print('IP-Address:', wlan.ifconfig()[0])

connect_wifi()
        
        
        
        
        
        
        
