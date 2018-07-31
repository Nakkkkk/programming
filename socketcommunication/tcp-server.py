#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from datetime import datetime
from time import sleep
import sys

s = socket.socket()

port = int(sys.argv[1])
s.bind(('10.0.1.32', port))
bef = 0


while True:
    print('listening')
    s.listen(5)
    c, addr = s.accept()
    print('receiving')
#    command_char = c.recv(4096)
#    command_int = int(command_char)

    command_int = int(c.recv(4096))

    print command_int + bef

    bef = command_int

#    if(command=='abc'):
#      print('packet is abc')
#    else:
#      print('not abc')
    
#    print('bef + aft = '+str(float(c.recv(4096))+bef))
#    print(c.recv(4096))
#    bef = float(c.recv(4096))
#    while True:
#        print('sending')
#        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#        try:
#            c.send(now)
#        except:
#            break
#        sleep(1)
    c.close()
s.close()
