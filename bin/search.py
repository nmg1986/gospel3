#!/usr/bin/python
#-*- coding:utf-8 -*-

from ConfigParser import SafeConfigParser
import urllib
import os
import filecmp

class SEARCH():
	def __init__(self):
			URL='http://192.168.4.198:8000/soft/list.server'
			filename='package/list.server'
			urllib.urlretrieve(URL,filename)
