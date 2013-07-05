#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import sqlite3
import os

class HeartBeatConfig(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)

		frame1=gtk.Frame('基本配置')
		frame2=gtk.Frame('进程监控')
		frame3=gtk.Frame('数据同步')
		frame4=gtk.Frame('邮件告警')

		self.add(frame1)
		self.add(frame2)
		self.add(frame3)
		self.add(frame4)

		self.conn=sqlite3.connect('db/server.db')
		self.index=0

		hbox=gtk.HBox()
		frame1.add(hbox)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		label=gtk.Label('主机')
		label.set_size_request(100,22)
		fixed.put(label,5,36)
		liststore=gtk.ListStore(str)
		cursor=self.conn.cursor()
		cursor.execute("select hostname from server where role='%s'" % self.index)
		while True:
			data=cursor.fetchone()
			if data is None:
				break
			host=str(data[0])
			liststore.append([host])
		cursor.close()
		combo=gtk.ComboBoxEntry(liststore)
		combo.set_size_request(150,25)
		fixed.put(combo,70,35)

		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		label=gtk.Label('备机')
		label.set_size_request(100,22)
		fixed.put(label,5,36)
		liststore=gtk.ListStore(str)
		cursor=self.conn.cursor()
		cursor.execute("select hostname from server where role='%s'" % self.index)
		while True:
			data=cursor.fetchone()
			if data is None:
				break
			host=str(data[0])
			liststore.append([host])
		cursor.close()
		combo=gtk.ComboBoxEntry(liststore)
		combo.set_size_request(150,25)
		fixed.put(combo,70,35)

		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		label=gtk.Label('虚拟IP')
		label.set_size_request(100,22)
		fixed.put(label,5,36)
		entry=gtk.Entry()
		entry.set_size_request(150,25)
		fixed.put(entry,75,35)

		vbox=gtk.VBox()
		hbox.pack_start(vbox,False,False,0)
		fixed=gtk.Fixed()
		vbox.pack_end(fixed,False,False,0)
		button=gtk.Button('高级设置')
		button.set_size_request(100,25)
		fixed.put(button,0,0)

		hbox=gtk.HBox()
		frame2.add(hbox)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		radio1=gtk.RadioButton(None,'开启')
		radio2=gtk.RadioButton(radio1,'关闭')
		fixed.put(radio1,40,35)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		fixed.put(radio2,40,35)
		vbox=gtk.VBox()
		hbox.pack_start(vbox,False,False,0)
		fixed=gtk.Fixed()
		vbox.pack_end(fixed,False,False,0)
		button=gtk.Button('高级设置')
		button.set_size_request(100,25)
		fixed.put(button,0,0)

		hbox=gtk.HBox()
		frame3.add(hbox)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		radio1=gtk.RadioButton(None,'开启')
		radio2=gtk.RadioButton(radio1,'关闭')
		fixed.put(radio1,40,35)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		fixed.put(radio2,40,35)
		vbox=gtk.VBox()
		hbox.pack_start(vbox,False,False,0)
		fixed=gtk.Fixed()
		vbox.pack_end(fixed,False,False,0)
		button=gtk.Button('高级设置')
		button.set_size_request(100,25)
		fixed.put(button,0,0)

		hbox=gtk.HBox()
		frame4.add(hbox)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		radio1=gtk.RadioButton(None,'开启')
		radio2=gtk.RadioButton(radio1,'关闭')
		fixed.put(radio1,40,35)
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		fixed.put(radio2,40,35)
		vbox=gtk.VBox()
		hbox.pack_start(vbox,False,False,0)
		fixed=gtk.Fixed()
		vbox.pack_end(fixed,False,False,0)
		button=gtk.Button('高级设置')
		button.set_size_request(100,25)
		fixed.put(button,0,0)

		hbox=gtk.HBox()
		fixed=gtk.Fixed()
		hbox.pack_start(fixed,True,True,0)
		statusbar=gtk.Statusbar()
		fixed.put(statusbar,0,0)
		fixed=gtk.Fixed()
		hbox.pack_end(fixed,False,False,0)
		button=gtk.Button('开始配置')
		button.set_size_request(100,25)
		button.connect('clicked',self.start_config)
		fixed.put(button,0,0)
		self.pack_end(hbox,False,False,0)

	def start_config(self,widget):
		pass	
