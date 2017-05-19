# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 15:14:46
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 16:04:39
import socket
from src.workers.base_worker import BaseWorker


class Dialer(BaseWorker):

    def __init__(self, service, mainbox):
        self.service = service
        self.mainbox = mainbox
        super(Dialer, self).__init__()

    def __del__(self):
        try:
            self.dialSocket.close()
        except AttributeError:
            pass

    def run(self):
        while True:
            msg = self.recv()
            self.dialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if msg['msg'] == 'dialReq':
                self.mainbox.put(('e', 'dialing.'))
                self.dialSocket.connect((msg['host'], msg['port']))
                self.dialSocket.send(msg['msg'].encode())
                res = self.dialSocket.recv(128).decode()
                if res == 'accept':
                    self.service.anwser(msg['host'], msg['port'] - 1)
                    # self.dialSocket.send('client_ready')
                    self.mainbox.put(('c', 'dial_accepted.'))
                elif res == 'deny':
                    self.mainbox.put(('c', 'denied'))
                self.dialSocket.close()
            elif msg['msg'] == 'hangUp':
                self.dialSocket.connect((msg['host'], msg['port']))
                self.dialSocket.send("{'code': 0, 'message': 'remote_hang_up}'".encode())
                self.mainbox.put(('c', 'hang_up'))
                self.dialSocket.close()
