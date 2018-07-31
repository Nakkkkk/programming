#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from contextlib import closing
import sys

s = socket.socket()

host = sys.argv[1]
port = int(sys.argv[2])
command = sys.argv[3]

#with closing(s):
s.connect((host, port))
s.send(command)
#while True:
#    print host, s.recv(4096)
