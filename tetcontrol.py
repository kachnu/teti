#!/usr/bin/python3
import os.path
import time
import threading
from TET import TETP6

config_file = 'config.py'
if os.path.isfile(config_file):
    print('Config file - OK')
    from config import *
else:
    print('Bad config')
    sensors = []
    sleeptime = 0.1
    cycletime = 10

TETs = []
with open('teti.csv') as f:
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

def opros_tet(tet):
    if tet.readDIs(sleeptime):
        tet.printTET(sensors)
        tet.check(len(sensors))

try:
    while True:
        for tet in TETs:
            t = threading.Thread(name=tet.name, target=opros_tet, args=(tet,))
            t.setDaemon(True)
            t.start()
            t.join
        time.sleep(cycletime)
        print('end cycle' + '  '+ str(threading.active_count()))

except KeyboardInterrupt:
    pass


