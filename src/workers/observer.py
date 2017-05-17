# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-18 00:51:14
import socket
import json
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
                self.connTransSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connTransSocket.connect((self.remoteAddr, self.PORT))
                self.connTransSocket.send("{'code': 0, 'message': 'remote_hang_up}'".encode())
                self.mainbox.put(('c', 'hang_up'))
            elif msg['msg'] == 'accept':
                self.service.anwser(msg['host'], msg['port'])
                self.connTransSocket.send('accept'.encode())
                self.send({'msg': 'wait'})
            elif msg['msg'] == 'deny':
                self.connTransSocket.send('deny'.encode())
                self.send({'msg': 'observe'})
            elif msg['msg'] == 'observe':
                self.connTransSocket, self.remoteAddr = self.connServerSocket.accept()
                message = self.connTransSocket.recv(128).decode()
                if message == 'dialReq':
                    self.mainbox.put(('c', 'dialReqRecv', self.remoteAddr[0]))
                elif message == 'deny':
                    self.mainbox.put(('c', 'remote_denied'))
            elif msg['msg'] == 'wait':
                connTransSocket, remoteAddr = self.connServerSocket.accept()
                if remoteAddr == self.remoteAddr:
                    self.connTransSocket = connTransSocket
                    message = json.loads(self.connTransSocket.recv(128).decode())
                    if message['message'] == 'remote_hang_up':
                        self.service.hangUp()
                        self.mainbox.put(('c', 'hang_up'))
                else:
                    pass
            else:
                pass
