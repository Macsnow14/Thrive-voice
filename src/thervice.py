# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-03 01:00:54
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 15:49:44
import fire
import time
import signal
import sys
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
        self._link = False
        signal.signal(signal.SIGINT, self._signalHandler)

        self.observer.start()
        self.observer.send({'msg': 'observe'})

    def __del__(self):
        self.dialer.close()
        self.observer.close()

    def _signalHandler(self, signal, stack):
        self.mainbox.put(('c', 'KeyboardInterruption'))

    def mainThread(self):
        while True:
            if not self.mainbox.empty():
                data = self.mainbox.get()
                if data[0] == 'c':
                    print('alive')
                    remoteAddr = None
                    if data[1] == 'dialReqRecv':
                        remoteAddr = data[2]
                        instruction = None
                        while instruction != 'accept' and instruction != 'deny':
                            instruction = input('Incoming telegram, accept or deny?\n')
                        if instruction == 'accept':
                            self.observer.send({'msg': instruction, 'host': remoteAddr, 'port': 12000})
                            self._link = True
                        else:
                            self.observer.send({'msg': instruction})
                            self._link = False
                    elif data[1] == 'denied':
                        print('remote denied')
                    elif data[1] == 'hang_up':
                        self.observer.send({'msg': 'observe'})
                        if data[2] == self.dialHost:
                            self._link = False
                            self.service.hangUp()
                            print('hang up')
                    elif data[1] == 'set_host':
                        self.dialHost = data[2]
                    elif data[1] == 'KeyboardInterruption':
                        print('alive-k')
                        if self._link:
                            print('alive-kl')
                            self.dialer.start()
                            self.dialer.send({'msg': 'hangUp', 'host': self.dialHost, 'port': 12001})
                        else:
                            instruction = None
                            while instruction != 'dial' and instruction != 'exit':
                                instruction = input('Do you wanna dial someone or exit?\n')
                            if instruction == 'dial':
                                print('to whom you want to call?')
                                self.dialHost = input('please input the host name.\n')
                                self.dialer.start()
                                self.dialer.send({'msg': 'dialReq', 'host': self.dialHost, 'port': 12001})
                                self._link = True
                            else:
                                sys.exit(0)
                elif data[0] == 'e':
                    print(data[1:])

            time.sleep(0.1)


if __name__ == '__main__':
    server = PhoneServer()
    fire.Fire(server)
