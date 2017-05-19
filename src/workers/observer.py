# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 16:00:41
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
            if msg['msg'] == 'accept':
                self.service.anwser(msg['host'], msg['port'])
                self.connTransSocket.send('accept'.encode())
                self.mainbox.put(('c', 'set_host', self.remoteAddr))
                self.send({'msg': 'observe'})
            elif msg['msg'] == 'deny':
                self.connTransSocket.send('deny'.encode())
                self.send({'msg': 'observe'})
            elif msg['msg'] == 'observe':
                self.connTransSocket, self.remoteAddr = self.connServerSocket.accept()
                message = self.connTransSocket.recv(128).decode()
                self.mainbox.put(('e', message))
                if message == 'dialReq':
                    self.mainbox.put(('c', 'dialReqRecv', self.remoteAddr[0]))
                elif message['message'] == 'remote_hang_up':
                    self.service.hangUp()
                    self.mainbox.put(('c', 'hang_up', self.remoteAddr))
                else:
                    pass
            else:
                pass
