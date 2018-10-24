#!/usr/bin/env python
# coding:utf8
# By:dub


import urllib.request
from xml.dom.minidom import parse, parseString
import xml.dom.minidom
import threading

import pymongo

from log.mylog import Mylog
#import db

mylog = Mylog()
mylog.debug('connection mongodb')

city_list_url = 'http://flash.weather.com.cn/wmaps/xml/%s.xml'
city_info = 'http://flash.weather.com.cn/wmaps/xml/%s.xml'


def mongodb():
    conn = pymongo.MongoClient()
    if 'weather' in conn.database_names():
        mylog.debug('database weather is exist!')
        if 'china' in conn['weather'].collection_names():
            collection = conn['weather']['china']
            mylog.debug('table china is exist!')
        else:
            collection = conn['weather']['china']
            mylog.debug('connection table china')
    else:
        mydb = conn['weather']
        collection = mydb['china']
        mylog.debug('create database weather and table china')
    return collection

collection = mongodb()

def getParseList(url=city_list_url,city='china', tag=None):
    url = url % city
    mylog.debug('get %s info' % url)
    data = urllib.request.urlopen(url)
    if data.url == url:
        content = data.read()
        dom = xml.dom.minidom.parseString(content)
        domList = dom.getElementsByTagName('city')
    else:
        domList = []
        mylog.error('get %s info faild' % url)
    return domList


def parseprov(dom):
    city_code = dom.getAttributeNode('quName').nodeValue
    city_cn = dom.getAttributeNode('cityname').nodeValue
    city_pin = dom.getAttributeNode('pyName').nodeValue
    city_detail = dom.getAttributeNode('stateDetailed').nodeValue
    city_teml = dom.getAttributeNode('tem1').nodeValue
    city_temh = dom.getAttributeNode('tem2').nodeValue
    city_list = {
            'city_code':city_code,
            'city_cn': city_cn,
            'city_pin': city_pin,
            'city_teml':city_teml,
            'city_temh':city_temh
            }
    mylog.debug('parse %s info ' % city_pin)
    return city_list

def update_city_list(domlist):
    for i in range(len(domlist)):
        dom = domlist[i]
        city_list = parseprov(dom)
        collection.insert_one(city_list)
        t = threading.Thread(target=update_city_info,
                args=(city_info,city_list['city_pin']))
        t.start()

def parseCh(domlist,pyName):
    mylog.debug('parse %s info detail' % pyName)
    child_list = []
    for i in range(len(domlist)):
        dom = domlist[i]
        city_name = dom.getAttributeNode('cityname').nodeValue
        city_pin = dom.getAttributeNode('pyName').nodeValue
        city_stat = dom.getAttributeNode('stateDetailed').nodeValue
        city_teml = dom.getAttributeNode('tem1').nodeValue
        city_temh = dom.getAttributeNode('tem2').nodeValue
        city_temn = dom.getAttributeNode('temNow').nodeValue
        city_win = dom.getAttributeNode('windState').nodeValue
        city_info = {
                'city_name': city_name,
                'city_pin': city_pin,
                'city_stat': city_stat,
                'city_teml': city_teml,
                'city_temh': city_temh,
                'city_temn': city_temn,
                'city_win': city_win
                }
        child_list.append(city_info)

    query = {'city_pin':{'$regex':pyName}}
    newquery = {'$set':{'child_info':child_list}}
    collection.update_one(query, newquery)


def update_city_info(city_info, city_pin):
    domlist = getParseList(city_info,city_pin)
    parseCh(domlist,city_pin)


def main():
    mylog.debug('main process start ')
    domlist = getParseList()
    if len(domlist):
        update_city_list(domlist)
    else:
        mylog.error('main process stop ')

if __name__ == '__main__':
    main()
