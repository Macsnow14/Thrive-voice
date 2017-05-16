# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-16 16:38:16
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-16 20:23:11
from src.workers.listener import Listener
from src.workers.player import Player
from src.workers.speaker import Speaker
from src.workers.recorder import Recorder


class VoiceService:
    inputFrames = []
    outputFrames = []

    def __init__(self):
        self.listener = Listener(self.inputFrames)
        self.player = Player(self.inputFrames)
        self.speaker = Speaker(self.outputFrames)
        self.recorder = Recorder(self.outputFrames)

    def __del__(self):
        self.hangUp()

    def anwser(self, host, port):
        self.listener.start()
        self.player.start()
        self.recorder.start()
        self.speaker.start()

        self.speaker.send((host, port))

        # self.listener.join()
        # self.player.join()
        # self.recorder.join()
        # self.speaker.join()

    def hangUp(self):
        self.listener.close()
        self.player.close()
        self.speaker.close()
        self.recorder.close()


if __name__ == "__main__":
    import time
    service = VoiceService()
    service.anwser('192.168.0.127', 12000)
    while True:
        time.sleep(0.1)
        # service.hangUp()
