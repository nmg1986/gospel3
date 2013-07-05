#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
import time
import urllib
import softcenter
from ConfigParser import SafeConfigParser
import os
import variables
import managesoftlist


URL='http://121.199.34.72/package'
LIST_NAME='list.server'
LIST_URL='%s/%s'%(URL,LIST_NAME)
SOFT_URL=URL
PKG_DIR='package'
class DownLoad(threading.Thread):
	def __init__(self,treeview,liststore,path):
         self.treeview=treeview
         self.model=treeview.get_model()
         self.treeiter=self.model.get_iter(path)
         self.liststore=liststore
         threading.Thread.__init__(self)
	def run(self):
		self.liststore.set_value(self.treeiter,6,'正在下载...')
		pkg_name=self.model.get_value(self.treeiter,1)
		'''
			delete the old version	
		'''
		if os.path.isfile('package/list.client'):
			parser=SafeConfigParser()
			parser.read('package/list.client')
			if parser.has_section(pkg_name):
				package=parser.get(pkg_name,'package').strip("'")
				if os.path.isfile('%s/%s'%(PKG_DIR,package)):
                                        os.remove('%s/%s'%(PKG_DIR,package))

		'''
			download the new version
		'''
		parser=SafeConfigParser()
		parser.read('package/list.server')
		package=parser.get(pkg_name,'package').strip("'")
		local=PKG_DIR + '/' + package
		url='%s/%s'%(SOFT_URL,package)
		urllib.urlretrieve(url,local,self.report)
		self.liststore.set_value(self.treeiter,6,'下载完成')
		self.liststore.set_value(self.treeiter,6,'最新')
		version=self.liststore.get_value(self.treeiter,4)
		self.liststore.set_value(self.treeiter,3,version)
		self.liststore.set_value(self.treeiter,7,0)
		self.treeview.get_selection().unselect_iter(self.treeiter)
		'''
			flush the flag
		'''
		variables.THREAD_NUM=variables.THREAD_NUM - 1
	def report(self,a,b,c):
		value=100*a*b/c
		if value > 100:
			value=100
		percent=str(value) + '%'
		self.liststore.set_value(self.treeiter,6,'%s'% percent)
class FlushModel(threading.Thread):
		def __init__(self,treeview):
			self.treeview=treeview
			threading.Thread.__init__(self)
		def run(self):
			self.treeview.get_model().clear()
			time.sleep(1)
			managesoftlist.ManageSoftList(self.treeview.get_model()).flush_soft_list()
class WaitAll(threading.Thread):
		def __init__(self,button,checkbox,treeview):
			self.button=button
			self.checkbox=checkbox
			self.treeview=treeview
			threading.Thread.__init__(self)
		def run(self):
			while True:
				if variables.THREAD_NUM == 0:
					self.update_soft_list()
					#T=FlushModel(self.treeview)
					#T.setDaemon(True)
					#T.start()
					self.button.set_sensitive(True)
					self.checkbox.set_sensitive(True)
					self.checkbox.set_active(False)
					break
				time.sleep(1)	
		def update_soft_list(self):
			if os.path.isfile('package/list.client'):
				os.remove('package/list.client')
			os.rename('package/list.server','package/list.client')
