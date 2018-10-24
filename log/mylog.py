#!/usr/bin/env python
# coding:utf8
# By:dub

import logging
LOG_FILE = '/var/log/mylog.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

class Mylog:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(LOG_FORMAT)
        self.loghandler = logging.FileHandler(LOG_FILE)
        self.loghandler.setFormatter(self.formatter)
        self.logger.addHandler(self.loghandler)


    def debug(self, msg):
        #self.logger.setLevel(logging.DEBUG)
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)


