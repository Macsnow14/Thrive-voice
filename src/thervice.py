# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-03 01:00:54
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-16 20:13:05
import fire
import time
from queue import Queue
from .services.voice_service import VoiceService
from .workers.dialer import Dialer
from .workers.observer import Observer


class PhoneServer(object):

    def __init__(self):
        # register a shutdown signal
        self.mainbox = Queue()
        self.service = VoiceService()
        self.observer = Observer(self.service, self.mainbox)
        self.dialer = Dialer(self.service, self.mainbox)
        # signal.signal(signal.SIGINT, self._signalHandler)

        self.observer.start()
        self.dialer.start()
        self.observer.send({'msg': 'observe'})

    def __del__(self):
        self.dialer.close()
        self.observer.close()

    # def _signalHandler(self, signal, stack):
    #     self.mainbox.put('')

    def mainThread(self, host=None, port=None, dial=False):
        if dial:
            self.dialer.send(('dialReq', host, port))
            while True:
                if not self.mainbox.empty():
                    data = self.mainbox.get()
                    if data[0] == 'c':
                        remoteAddr = None
                        if data[1] == 'dialReqRecv':
                            remoteAddr = data[2]
                        instruction = None
                        while instruction != 'accept' or 'deny':
                            instruction = input('Incoming telegram, accept or deny?')
                        self.observer.send({'msg': instruction, 'host': remoteAddr, 'port': 12000})
                    elif data[0] == 'e':
                        print(data[1])
        else:
            while True:
                if not self.mainbox.empty():
                    data = self.mainbox.get()
                    if data[0] == 'c':
                        remoteAddr = None
                        if data[1] == 'dialReqRecv':
                            remoteAddr = data[2]
                        instruction = None
                        while instruction != 'accept' or 'deny':
                            instruction = input('Incoming telegram, accept or deny?')
                        self.observer.send({'msg': instruction, 'host': remoteAddr, 'port': 12000})
                    elif data[0] == 'e':
                        print(data[1])

                time.sleep(0.1)
                # print('alive')


if __name__ == '__main__':
    server = PhoneServer()
    fire.Fire(server)
