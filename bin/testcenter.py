#!/usr/bin/python
# -*- coding:utf-8 -*-


import gtk
import hatest

class TestCenter(gtk.Notebook):
	def __init__(self):
		gtk.Notebook.__init__(self)

		vbox=hatest.HaTestCenter()
		label=gtk.Label('HA双机测试')
		self.append_page(vbox,label)
		
