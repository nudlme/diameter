#-*- coding: utf-8 -*-
#!/usr/bin/python

from sctp import *

class SCTPSocket():
    def __init__(self, host, port, num):
        self.host = host
        self.port = port
        self.num = num 
        self.socket = None

    def open(self):
        self.socket = sctpsocket_tcp(socket.AF_INET)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.num)

    def close(self):
        self.socket.close()

    def connect(self):
        self.socket = sctpsocket_tcp(socket.AF_INET)
        self.socket.connect((self.host, self.port))

    def accept(self):
        if self.num == 0:
            return None, None
        else:
            self.num -= 1
        return self.socket.accept()

    def send(self, buf):
        self.socket.sendall(buf)

    def recv(self):
        try:
            buf = self.socket.recv(1024)
        except ConnectionResetError:
            self.close()
            return None
        return buf