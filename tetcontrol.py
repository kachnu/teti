#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import time
import threading
from TET import TETP6
from loggerTET import logger

config_file = 'config.py'
if os.path.isfile(config_file):
    logger.info('Config file - OK')
    from config import *
else:
    logger.warning('Config file doesn"t exist. Default settings were applied')
    sensors = []
    sleeptime = 0.1
    cycletime = 10
    session_time = 5

TETs = []

if os.path.isfile('teti.csv'):
    teti_file = 'teti.csv'
else:
    logger.warning('File teti.csv doesn"t exist')
    teti_file = input('Enter file name: ')

with open(teti_file) as f:
    for line in f:
        if not line.startswith('#'):
            words = line.split(';')
            name = str(words[0])
            info = str(words[1])
            type_tet = str(words[2])
            ip = str(words[5])
            normal_state = (words[6])
            if type_tet.lower() == 'tet-p6' and type_tet !='':
                tet = TETP6(ip, name, info, normal_state)
                TETs.append(tet)
f.close()

logger.info('Request cicle is starting')
try:
    while True:
        for tet in TETs:
            t = threading.Thread(name=tet.name, target=tet.readDIs, args=(sleeptime,session_time))
            t.setDaemon(True)
            t.start()
        time.sleep(cycletime)
        
        for tet in TETs:
            if len(tet.currentDIs) > 0 :
                #tet.printTET(sensors)
                tet.check(sensors)

except KeyboardInterrupt:
    logger.info('Request cicle is stopped')
    pass


