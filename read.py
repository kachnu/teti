#!/usr/bin/python2
import re
import dryscrape
from bs4 import BeautifulSoup
import time


session = dryscrape.Session()
session.visit("http://10.99.95.201/login.cgi?webpwd=Admin&Submit=Submit")
time.sleep(0.5)
response = session.body()
soup = BeautifulSoup(response, 'lxml')

DIs = soup.findAll(id = re.compile('DI\d+'))
#DIs = soup.findAll(id = 'DI0')

i=0
for DI in DIs:
    if DI.text != '-':
        print('DI' + str(i) + ' ' + DI.text)
        i = i + 1
