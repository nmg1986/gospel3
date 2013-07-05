#!/usr/bin/python
# -*- coding:utf-8 -*- 


import gtk
import InputConfig
import MiddleWare
import IncuBation
import AppPortal
import ManagePlatForm
import DatabaseConfig



class ConfigManager(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)

		self.notebook=gtk.Notebook()
		self.add(self.notebook)

		vbox=InputConfig.InputConfig()
		label=gtk.Label('接入服务器配置')
		self.notebook.append_page(vbox,label)

		vbox=MiddleWare.MiddleWareConfig()
		label=gtk.Label('中间件服务器配置')
		self.notebook.append_page(vbox,label)

		vbox=ManagePlatForm.ManagePlatConfig()
		label=gtk.Label('管理平台配置')
		self.notebook.append_page(vbox,label)

		vbox=IncuBation.IncuBationConfig()
		label=gtk.Label('孵化平台配置')
		self.notebook.append_page(vbox,label)

		vbox=AppPortal.AppPortalConfig()
		label=gtk.Label('应用门户配置')
		self.notebook.append_page(vbox,label)

		vbox=DatabaseConfig.DatabaseConfig()
		label=gtk.Label('数据库服务器配置')
		self.notebook.append_page(vbox,label)
