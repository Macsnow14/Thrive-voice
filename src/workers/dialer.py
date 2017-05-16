# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 15:14:46
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-16 17:30:24
import socket
from src.workers.base_worker import BaseWorker


class Dialer(BaseWorker):

    def __init__(self, service, mainbox):
        self.dialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service = service
        self.mainbox = mainbox
        super(Dialer, self).__init__()

    def __del__(self):
        try:
            self.dialSocket.close()
        except AttributeError:
            pass

    def run(self):
        msg, host, port = self.recv()
        self.dialSocket.connect((host, port))
        self.dialSocket.send(msg)
        res = self.dialSocket.recv(128).decode()
        if res == 'accept':
            self.service.anwser(host, port)
            self.dialSocket.send('client_ready')
        elif res == 'deny':
            self.mainbox.put((1, 'dial request denied.'))
