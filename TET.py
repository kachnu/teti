#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import dryscrape
from bs4 import BeautifulSoup
import time
from loggerTET import logger


class TETP6:
    def __init__(self, ip, name, info, nDIs):
        self.numDI = 6
        self.ip = ip
        self.name = name
        self.info = info
        self.normalDIs = nDIs
        self.currentDIs = []
        self.timestamp = 0

    def readDIs(self, sleeptime, session_time):
        session = dryscrape.Session()
        session.set_timeout(session_time)
        url = 'http://' + self.ip + '/login.cgi?webpwd=Admin&Submit=Submit'
        try:
            session.visit(url)
            time.sleep(sleeptime)
        except:
            logger.warning('Destination Host Unreachable ' + self.name + ' IP: ' + self.ip)
            return False
        response = session.body()
        soup = BeautifulSoup(response, 'lxml')
        cDIs = soup.findAll(id = re.compile('DI\d+'))

        for DI in cDIs:
            if DI.text == 'ON':
                self.currentDIs.append(1)
            else:
                self.currentDIs.append(0)
        self.timestamp = time.ctime()
        return True

    def check(self, sensors):
        num = len(sensors)
        if num == 0:
            num = self.numDI
        for i in range(num):
            if str(self.normalDIs[i]) != str(self.currentDIs[i]):
                logger.warning(self.name + ' IP: ' + self.ip + ' ' + str(sensors[i]) + ' - ERROR')

    def printTET(self, sensors):
        if len(sensors) > 0:
            num = len(sensors)
            print(self.info + ' ' + self.timestamp)
            for i in range(num):
                print('DI' + str(i) + ' ' + str(sensors[i]) + ' ' + str(self.currentDIs[i]) + ' ' + str(self.normalDIs[i]))
        else:
            num = self.numDI-1
            print(self.info + ' ' + self.timestamp)
            for i in range(num):
                print('DI' + str(i) + ' ' + str(self.currentDIs[i]) + ' ' + str(self.normalDIs[i]))


