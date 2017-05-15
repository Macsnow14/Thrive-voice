# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 15:14:46
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 16:19:39
import socket
from src.threads.base_worker import BaseWorker


class Dialer(BaseWorker):

    def __init__(self, queue, port, host):
        self.PORT = port
        self.dialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(Dialer, self).__init__(queue)

    def __del__(self):
        try:
            self.dialSocket.close()
        except AttributeError:
            pass

    def run(self):
        self.dialSocket.connect((self.host, self.port))
        self.dialSocket.send('dialReq')
        res = self.dialSocket.recv(128).decode()
        if res == 'accept':
            self.listener()
            self.speaker(self.host, self.port)
            self.dialSocket.send('client_ready')
        elif res == 'deny':
            print('dial request denied.')
