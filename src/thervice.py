# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-03 01:00:54
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 16:12:05
import fire
import queue
import signal
import time
from threading import Thread


class PhoneServer(object):
    inputFrames = []
    outputFrames = []
    queue = queue.Queue()
    threads = []

    def __init__(self):
        # register a shutdown signal
        signal.signal(signal.SIGINT, self._signalHandler)

    def _signalHandler(self, signal, stack):
        self.queue.put_nowait('stop')

    def listen(self):
        inputStream = Thread(target=self.inputStream)
        play = Thread(target=self.play)
        inputStream.setDaemon(True)
        play.setDaemon(True)
        inputStream.start()
        play.start()
        self.threads.append(inputStream)
        self.threads.append(play)

    def speak(self, host, server_port):
        record = Thread(target=self.record)
        outputStream = Thread(target=self.outputStream, args=(host, server_port))
        record.setDaemon(True)
        outputStream.setDaemon(True)
        record.start()
        outputStream.start()
        self.threads.append(outputStream)
        self.threads.append(record)

    def mainThread(self):
        # should listen to TCP connection req for dial
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'dialReqRecv':
                    instruction = None
                    while instruction != 'accept' or 'deny':
                        instruction = input('Incoming telegram, accept or deny?')
                    self.queue.put_nowait(instruction)
                elif data == 'dialReqSend':
                    pass
                else:
                    self.queue.put_nowait(data)
            time.sleep(0.1)


if __name__ == '__main__':
    fire.Fire(PhoneServer)
