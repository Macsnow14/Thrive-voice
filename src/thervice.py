# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-03 01:00:54
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-04 02:31:16
import socket
import pyaudio
import fire
import queue
import time
from threading import Thread


class PhoneServer(object):
    BUFFER = 1024
    FREAM_BUFFER = 10
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    inputFrames = []
    outputFrames = []
    queue = queue.Queue()
    threads = []
    p = pyaudio.PyAudio()

    def __init__(self, listen_port=12000):
        self.PORT = listen_port
        print(type(listen_port))
        self.voiceServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.voiceClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.voiceServerSocket.bind(('127.0.0.1', self.PORT))
        self.connServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connServerSocket.bind(('127.0.0.1', self.PORT + 1))
        self.connServerSocket.listen(5)
        self.connTransSocket, addr = self.connServerSocket.accept()
        print('listen for call on port %d' % (self.PORT))
        dialReqlistener = Thread(target=self.dialReqlistener)
        dialReqlistener.setDaemon(True)
        dialReqlistener.start()
        self.threads.append(dialReqlistener)

    def __del__(self):
        self.voiceServerSocket.close()
        self.voiceClientSocket.close()
        self.connServerSocket.close()
        self.connTransSocket.close()

    def inputStream(self):
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_receive':
                    break
                else:
                    self.queue.put(data)
            soundData, addr = self.voiceServerSocket.recvfrom(self.BUFFER * self.CHANNELS * 2)
            self.inputFrames.append(soundData)

    def outputStream(self, host, server_port):
        print('port is %s on host %s' % (server_port, host))
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_send':
                    break
                else:
                    self.queue.put(data)
            if len(self.outputFrames) > 0:
                self.voiceClientSocket.sendto(self.outputFrames.pop(0), (host, server_port))

    def record(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_record':
                    break
                else:
                    self.queue.put(data)
            self.outputFrames.append(stream.read(self.BUFFER))

    def play(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             output=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_play':
                    break
                else:
                    self.queue.put(data)
            if len(self.inputFrames) == self.FREAM_BUFFER:
                while True:
                    if len(self.inputStream) == 0:
                        break
                    stream.write(self.inputFrames.pop(0), self.BUFFER)

    def listener(self):
        inputStream = Thread(target=self.inputStream)
        play = Thread(target=self.play)
        inputStream.setDaemon(True)
        play.setDaemon(True)
        inputStream.start()
        play.start()
        self.threads.append(inputStream)
        self.threads.append(play)

    def speaker(self, host, server_port):
        record = Thread(target=self.record)
        outputStream = Thread(target=self.outputStream, args=(host, server_port))
        record.setDaemon(True)
        outputStream.setDaemon(True)
        record.start()
        outputStream.start()
        self.threads.append(outputStream)
        self.threads.append(record)

    def dialReqlistener(self):
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'invisibility':
                    break
                else:
                    self.queue.put(data)
            message = self.connTransSocket.recv(128).decode()
            if eval(message)[0] == 'dial':
                self.queue.put('dialReq')

    def dialReq(self, host, port):
        dialSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dialSocket.connect((host, port))
        dialSocket.send('dialReq')
        res = dialSocket.recv(128).decode()
        if res == 'accept':
            pass
        elif res == 'deny':
            pass

    def mainThread(self):
        # should listen to TCP connection req for dial
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'dialReq':
                    input('')
                else:
                    self.queue.put(data)
            time.sleep(0.1)


if __name__ == '__main__':
    fire.Fire(PhoneServer)
