#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import time
import threading
from TET import TETP6
import logging

# создаём объект с именем модуля
logger = logging.getLogger(__name__)
# создаём обрабочтик файла лога
handler = logging.FileHandler('logger1.log')
# задаём уровень логгирования
handler.setLevel(logging.INFO)
# форматируем записи
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# устанавливаем формат для обработчика
handler.setFormatter(formatter)
# добавляем обработчик к логгеру
logger.addHandler(handler)


config_file = 'config.py'
if os.path.isfile(config_file):
    #print('Config file - OK')
    logger.info('Config file was readed successfully')
    from config import *
else:
    #print('Bad config')
    logger.warning('Config file doesn"t exist. Default settings are used')
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

try:
    while True:
        for tet in TETs:
            t = threading.Thread(name=tet.name, target=tet.readDIs, args=(sleeptime,session_time))
            t.setDaemon(True)
            t.start()
        time.sleep(cycletime)
        
        for tet in TETs:
            if len(tet.currentDIs) > 0 :
                tet.printTET(sensors)
                tet.check(len(sensors))
            
        #print('end cycle' + '  '+ str(threading.active_count()))

except KeyboardInterrupt:
    pass


