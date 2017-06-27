#!/usr/bin/python2
import re
import dryscrape
from bs4 import BeautifulSoup
import time


def read_DIs(ip, name, normal_state):
    session = dryscrape.Session()
    url = 'http://' + ip + '/login.cgi?webpwd=Admin&Submit=Submit' 
    print("")
    print(name)
    session.visit(url)
    time.sleep(0.1)
    response = session.body()
    soup = BeautifulSoup(response, 'lxml')
    DIs = soup.findAll(id = re.compile('DI\d+'))
    sensors = ["220V","SMOKE","DOOR","MUX LOS","",""]
    i=0
    for DI in DIs:
        if DI.text != '-':
            if DI.text == 'ON':
                DIT = 1
            else:
                DIT = 0
            print('DI' + str(i) + ' ' + sensors[i] + ' ' +str(DIT) + ' ' + normal_state[i])
            i = i + 1
    return

with open('teti.csv') as f:
    for line in f:
        if not line.startswith('#'):
            words = line.split(';')
            name = str(words[1])
            ip = str(words[5])
            normal_state = str(words[6])
            read_DIs(ip, name, normal_state)
f.close()


