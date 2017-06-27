#!/usr/bin/python2
import re
import dryscrape
from bs4 import BeautifulSoup
import time


def read_DIs(ip):
    session = dryscrape.Session()
    url = 'http://' + ip + '/login.cgi?webpwd=Admin&Submit=Submit' 
    print('Retrieving ' + url)
    session.visit(url)
    #session.set_timeout(0.5)
    time.sleep(0.5)
    response = session.body()
    soup = BeautifulSoup(response, 'lxml')
    DIs = soup.findAll(id = re.compile('DI\d+'))
    i=0
    for DI in DIs:
        if DI.text != '-':
            print('DI' + str(i) + ' ' + DI.text)
            i = i + 1
    return

with open('teti.csv') as f:
    for line in f:
        if not line.startswith('#'):
            words = line.split(';')
            ip = str(words[5])
            read_DIs(ip)
f.close()


