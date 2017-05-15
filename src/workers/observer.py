# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 15:57:50
import socket
from src.threads.base_worker import BaseWorker


class Observer(BaseWorker):

    def __init__(self, queue, port=12001):
        self.PORT = port
        self.connServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connServerSocket.bind(('127.0.0.1', self.PORT))
        self.connServerSocket.listen(5)
        self.connTransSocket = None
        super(Observer, self).__init__(queue)

    def __del__(self):
        try:
            self.connServerSocket.close()
            self.connTransSocket.close()
        except AttributeError:
            pass

    def run(self):
        self.connTransSocket, self.remoteAddr = self.connServerSocket.accept()
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'invisibility':
                    break
                elif data == 'accept':
                    self.queue.put_nowait('start_listen')
                elif data == 'server_ready':
                    self.connTransSocket.send('accept')
                    message = self.connTransSocket.recv(128).decode()
                    if message == 'client_ready':
                        self.queue.put_nowait('speak')
                elif data == 'deny':
                    self.connServerSocket.send('deny')
                elif data == 'observe':
                    message = self.connTransSocket.recv(128).decode()
                    if eval(message)[0] == 'dialReq':
                        self.queue.put_nowait('dialReqRecv')
                else:
                    self.queue.put_nowait(data)
