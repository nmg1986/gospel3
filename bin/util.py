#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
import glob
from ssh import *
import time
import os
import sqlite3
PKG_DIR='package/'
REMOTE_DIR='/opt/'
class INSTALL(threading.Thread):
	def __init__(self,treemodel,treeiter,liststore):
		self.model=treemodel
		self.treeiter=treeiter
		self.liststore=liststore
		self.host=self.model.get_value(self.treeiter,1)
		index=self.model.get_value(self.treeiter,3)
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
					select port,username,password,package 
					from server where hostname='%s' and role='%s'
				  ''' %(self.host,index)
				) 
		data=c.fetchone()
		self.port=int(data[0])
		self.username=str(data[1])
		self.password=str(data[2])
		self.package=data[3].replace(' ','').replace('[','').replace(']','').replace("'","").split(',')
		conn.close()
		threading.Thread.__init__(self)
	def run(self):
		if self.treeiter is not None:
			self.install()	
	def install(self):
                path=self.liststore.get_path(self.treeiter)
                print path
		self.liststore.set_value(self.treeiter,7,'--')
		ssh=SSHClient()
		self.liststore.set_value(self.treeiter,6,'正在连接服务器')
		rc=ssh.connect(self.username,self.password,self.host,self.port)	
		if rc == 0:
			self.liststore.set_value(self.treeiter,6,'成功建立连接')
		else:
			self.liststore.set_value(self.treeiter,6,'连接失败')
			return
		time.sleep(2)
		for package in self.package:
                        package=package.split('-')[0]
			self.liststore.set_value(self.treeiter,6,'正在上传%s安装包' % package)
			localfile=os.path.join(PKG_DIR,package)
			remotefile=os.path.join(REMOTE_DIR,package)
			ssh.upload(localfile,remotefile)
			time.sleep(2)
			self.liststore.set_value(self.treeiter,6,'上传成功')
			time.sleep(2)
			self.liststore.set_value(self.treeiter,6,'正在解压%s安装包' % package)
			rc=ssh.execute('tar -xzmf %s -C %s' % (remotefile,REMOTE_DIR))
			time.sleep(3)
			if rc == 0:
				self.liststore.set_value(self.treeiter,6,'解压%s成功'%package)
			else:
				self.liststore.set_value(self.treeiter,6,'解压%s失败'%package)
				return
			time.sleep(1)
			self.liststore.set_value(self.treeiter,6,'正在部署%s' % package)
			rc=ssh.execute('cd %s/%s;./install' % (REMOTE_DIR,package))
			if rc == 0:
				self.liststore.set_value(self.treeiter,6,'部署%s成功'%package)
			else :
				self.liststore.set_value(self.treeiter,6,'部署%s失败'%package)
				self.liststore.set_value(self.treeiter,7,'×')
				return
		self.liststore.set_value(self.treeiter,6,'部署成功')
		self.liststore.set_value(self.treeiter,7,'√')
		path=self.liststore.get_path(self.treeiter)
		
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute("update server set progress='%s',status='1' where rowid='%s'"%(path[0],'部署成功'))

class UPDATE(threading.Thread):
     def __init__(self,treeview,liststore,path):
         self.model=treeview.get_model()
         self.treeiter=self.model.get_iter(path)
         self.liststore=liststore
         threading.Thread.__init__(self)
     def run(self):
		self.liststore.set_value(self.treeiter,5,'检查更新...')
		time.sleep(3)
		self.liststore.set_value(self.treeiter,5,'正在更新...')
		time.sleep(3)
		self.liststore.set_value(self.treeiter,5,'更新完毕')
