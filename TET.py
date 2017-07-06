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
        self.link = False
        self.ERRORS = dict()
        
        
    def readDIs(self, sleeptime, session_time):
        session = dryscrape.Session()
        session.set_timeout(session_time)
        url = 'http://' + self.ip + '/login.cgi?webpwd=Admin&Submit=Submit'
        try:
            session.visit(url)
            time.sleep(sleeptime)
            self.link = True
            self.timestamp = time.time()
        except:
            newError = 'Destination Host Unreachable ' + self.name + ' IP: ' + self.ip
            if newError not in self.ERRORS:
                logger.warning(newError)
                self.ERRORS[newError] = time.time()
            return False
        response = session.body()
        soup = BeautifulSoup(response, 'lxml')
        cDIs = soup.findAll(id = re.compile('DI\d+'))
        self.currentDIs = []
        for DI in cDIs:
            if DI.text == 'ON':
                self.currentDIs.append(1)
            else:
                self.currentDIs.append(0)
        return True

    def check(self, sensors):
        if self.link:
            num = len(sensors)
            if num == 0:
                num = self.numDI
            count = num
            for i in range(num):
                if str(self.normalDIs[i]) != str(self.currentDIs[i]):
                    newError = self.name + ' IP: ' + self.ip + ' ' + str(sensors[i]) + ' - ERROR'
                    count = count - 1
                    
                    if newError not in self.ERRORS:
                        self.ERRORS[newError] = time.time()
                        logger.warning(newError)
        if count == num:
            if len(self.ERRORS) > 0:
                for e in self.ERRORS:
                    logger.warning(e + ' - OK')
                self.ERRORS = dict()




