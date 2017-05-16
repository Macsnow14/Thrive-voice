# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-03 01:00:54
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-16 18:07:36
import fire
import signal
import time
from queue import Queue
from .services.voice_service import VoiceService
from .workers.dialer import Dialer
from .workers.observer import Observer


class PhoneServer(object):

    def __init__(self):
        # register a shutdown signal
        self.mainbox = Queue()
        self.observer = Observer(self.queue)
        self.services = VoiceService()
        signal.signal(signal.SIGINT, self._signalHandler)

        self.observer.start()
        self.observer.send({'msg': 'observe'})

    def _signalHandler(self, signal, stack):
        self.queue.put_nowait('stop')

    def mainThread(self):
        # should listen to TCP connection req for dial
        while True:
            if not self.mainbox.empty():
                data = self.queue.get()
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
                    pass


            time.sleep(0.1)


if __name__ == '__main__':
    fire.Fire(PhoneServer)
