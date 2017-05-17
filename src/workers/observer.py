# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-17 14:14:57
import socket
from src.workers.base_worker import BaseWorker


class Observer(BaseWorker):

    def __init__(self, service, mainbox, port=12001):
        self.PORT = port
        self.connServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connServerSocket.bind(('', self.PORT))
        self.connServerSocket.listen(5)
        self.connTransSocket = None
        self.mainbox = mainbox
        self.service = service
        super(Observer, self).__init__()

    def __del__(self):
        try:
            self.connServerSocket.close()
            self.connTransSocket.close()
        except AttributeError:
            pass

    def run(self):
        while True:
            msg = self.recv()
            if msg['msg'] == 'hangUp':
                self.service.hangUp()
                try:
                    self.connTransSocket.send("{'code': 0, 'massage': 'remote_hang_up'")
                except AttributeError:
                    pass
            elif msg['msg'] == 'accept':
                self.service.anwser(msg['host'], msg['port'])
                self.connTransSocket.send('accept'.encode())
            elif msg['msg'] == 'deny':
                self.connTransSocket.send('deny'.encode())
            elif msg['msg'] == 'observe':
                self.connTransSocket, self.remoteAddr = self.connServerSocket.accept()
                message = self.connTransSocket.recv(128).decode()
                if message == 'dialReq':
                    self.mainbox.put(('c', 'dialReqRecv', self.remoteAddr[0]))
                elif message == 'deny':
                    self.mainbox.put(('c', 'remote_denied'))
            else:
                pass
