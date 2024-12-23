#!/usr/bin/python

import socket, select
from Server import RocServer
import signal
import sys

def signal_handler(sig, frame):
    print('[INFO] Shutdown server ! ')
    server.close()
    sys.exit(0)


host = ''
port = 5555

server = RocServer(host, port)

#connection.send('<fb id="fb1" state="true"/>\n'.encode('utf-8'))

signal.signal(signal.SIGINT, signal_handler)


while 1:
        server.update()
