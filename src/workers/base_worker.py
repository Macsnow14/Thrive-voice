# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:03:39
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:15:25


class BaseWorker(object):
    queue = None

    def __init__(self, queue):
        self.queue = queue
        super(BaseWorker, self).__init__()

    def run(self):
        raise NotImplementedError
