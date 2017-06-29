#!/usr/bin/python3
import re
import dryscrape
from bs4 import BeautifulSoup
import time


class TETP6:
    def __init__(self, ip, name, info, nDIs):
        self.numDI = 6
        self.ip = ip
        self.name = name
        self.info = info
        self.normalDIs = nDIs
        self.currentDIs = []
        self.timestamp = 0

    def readDIs(self, sleeptime):
        session = dryscrape.Session()
        url = 'http://' + self.ip + '/login.cgi?webpwd=Admin&Submit=Submit'
        try:
            print("Try connect" + ' - '+ self.name)
            session.visit(url)
            time.sleep(sleeptime)
        except:
            print('Error connect' + ' - ' + self.name)
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

    def check(self, num):
        n = 0
        if num == 0:
            num = self.numDI
        for i in range(num):
            #print(str(self.normalDIs[i]) + ' ' + str(self.currentDIs[i]))
            if str(self.normalDIs[i]) != str(self.currentDIs[i]):
                n = n + 1
        #print(self.info + ' ' + self.timestamp)
        if n == 0:
            print('Status OK')
        else:
            print('Status ATTENTION!  ERROR ERROR ERROR  ATTENTION!')

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


