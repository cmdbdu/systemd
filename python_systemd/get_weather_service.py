#!/usr/bin/env python
# coding:utf8
# By:dub

import os
import sys
import logging
import schedule
import time

try:
    sys.path.append(os.path.abspath('..'))
    from weather.get_weather import main
    from log.mylog import Mylog
except Exception as e:
    sys.path.append('/home/dub/crawl_china_weather_every_six_hour')
    from weather.get_weather import main
    from log.mylog import Mylog


def run():
    schedule.every(2).hours.do(main)
    mylog = Mylog()
    while True:
        schedule.run_pending()
        time.sleep(3600)
        mylog.debug('next_run @%s' % schedule.next_run() )

if __name__ == "__main__":
    run()
