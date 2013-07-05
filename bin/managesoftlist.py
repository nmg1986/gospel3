#!/usr/bin/python
#-*- coding:utf-8 -*-
import urllib
import os
from ConfigParser import SafeConfigParser
import gtk


class ManageSoftList():
		def __init__(self,liststore):
			self.liststore=liststore
			self.url='http://121.199.34.72/package/list.server'
		def get_soft_list(self):
			filename='package/list.server'
			try:
				urllib.urlretrieve(self.url,filename)
			except IOError:
			        text='无法连接服务器,请检查网络设置'
			        md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,text)
				md.run()
				md.destroy()
				print text 
				if os.path.isfile('package/list.server'):
					parser=SafeConfigParser()
					parser.read('package/list.server')
					for section in parser.sections():
						name=section
						desc=parser.get(section,'description').strip("'")
						size=parser.get(section,'size').strip("'")
						version=parser.get(section,'version').strip("'")
						self.liststore.append([False,name,desc,version,version,size,'未知',0])
				return
			if not os.path.isfile('package/list.client'):
				parser=SafeConfigParser()
				parser.read('package/list.server')
				for section in parser.sections():
					name=section
					desc=parser.get(section,'description').strip("'")
					size=parser.get(section,'size').strip("'")
					version=parser.get(section,'version').strip("'")
					self.liststore.append([False,name,desc,'---',version,size,'下载',1])
			else:
				serverparser=SafeConfigParser()
				serverparser.read('package/list.server')
				clientparser=SafeConfigParser()
				clientparser.read('package/list.client')
				for section in serverparser.sections():
					if clientparser.has_section(section):
						clientversion=clientparser.get(section,'version').strip("'")	
						serverversion=serverparser.get(section,'version').strip("'")
						if (clientversion >= serverversion):
							name=section
							desc=clientparser.get(section,'description').strip("'")
							size=clientparser.get(section,'size').strip("'")	
							self.liststore.append([False,name,desc,clientversion,serverversion,size,'最新',0])
						else:
							name=section
							desc=serverparser.get(section,'description').strip("'")
							size=serverparser.get(section,'size').strip("'")
							self.liststore.append([False,name,desc,clientversion,serverversion,size,'立即更新',1])
					else:
						name=section
						desc=serverparser.get(section,'description').strip("'")
						size=serverparser.get(section,'size').strip("'")
						version=serverparser.get(section,'version').strip("'")
						self.liststore.append([False,name,desc,'---',version,size,'下载',1])
		def flush_soft_list(self):
			parser=SafeConfigParser()
			parser.read('package/list.client')
			for section in parser.sections():
				name=section
				desc=parser.get(section,'description').strip("'")
				size=parser.get(section,'size').strip("'")
				version=parser.get(section,'version').strip("'")
				self.liststore.append([False,name,desc,version,version,size,'最新',0])
			
		def msg(self,text):
			md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,
								gtk.BUTTONS_OK,text)
			md.run()
			md.destroy()
				
