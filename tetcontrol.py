#!/usr/bin/python3
import os.path
import time
from TET import TET6

config_file = 'config.py'
if os.path.isfile(config_file):
    print('OK config')
    from config import *
else:
    print('Bad config')
    sensors = []
    sleeptime = 0.1


TETs = []
with open('teti.csv') as f:
    for line in f:
        if not line.startswith('#'):
            words = line.split(';')
            name = str(words[0])
            ip = str(words[5])
            info = str(words[1])
            normal_state = (words[6])
            tet = TET6(ip, name, info, normal_state)
            #tet.readDIs(sleeptime)
            TETs.append(tet)
f.close()

try:
    while True:
        for tet in TETs:
            tet.readDIs(sleeptime)
            tet.printTET(sensors)
            tet.check(len(sensors))
        time.sleep(5)   
except KeyboardInterrupt:
    pass


