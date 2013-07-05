#!/usr/bin/python
# -*- coding:utf-8 -*-

import gtk
import bin.softcenter as softcenter
import bin.serverpool as serverpool
import bin.deploy as deploy
import bin.configmanager as configmanager
import bin.testcenter as testcenter
import bin.operation as operation

#MAIN_WINDOW_WIDTH=915
#MAIN_WINDOW_HEIGHT=614
MAIN_WINDOW_WIDTH=850
MAIN_WINDOW_HEIGHT=600

class Gospel(gtk.Window):
	def __init__(self):
		super(Gospel,self).__init__()

		self.set_size_request(MAIN_WINDOW_WIDTH,MAIN_WINDOW_HEIGHT)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_resizable(False)
		self.connect("delete-event",gtk.main_quit)
		
		actiongroup=gtk.ActionGroup('myaction')
		
		softaction=gtk.RadioAction('soft','_软件仓库','软件仓库',None,0)
		softaction.set_active(True)
		softaction.connect('activate',self.soft_center)
		#label=gtk.Image()
		#label.set_from_file('icon/nginx.gif')
		#softaction.connect_proxy(label)
		#actiongroup.add_action(softaction)
		#actiongroup.add_action(deployaction)

		deployaction=gtk.RadioAction('deploy','_安装部署','安装部署',None,1)
		#actiongroup.add_action(deployaction)
		deployaction.set_group(softaction)
		deployaction.connect('activate',self.deploy_center)

		configaction=gtk.RadioAction('config','_配置中心','配置管理',None,2)	
		configaction.set_group(softaction)
		configaction.connect('activate',self.config_center)

		testaction=gtk.RadioAction('test','_测试中心','测试中心',None,3)
		testaction.set_group(softaction)
		testaction.connect('activate',self.test_center)

		yunweiaction=gtk.RadioAction('yunwei','_运维中心','运维中心',None,4)
		yunweiaction.set_group(softaction)
		yunweiaction.connect('activate',self.yunwei_center)
		

		self.toolbar=gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_ICONS)

		quittb=gtk.ToolButton(gtk.STOCK_QUIT)
		quittb.connect('clicked',gtk.main_quit)
		self.toolbar.insert(quittb,-1)

		softitem=softaction.create_tool_item()
		softitem.set_size_request(80,50)
		self.toolbar.insert(softitem,-1)

		deployitem=deployaction.create_tool_item()
		deployitem.set_size_request(80,50)
		self.toolbar.insert(deployitem,-1)

		configitem=configaction.create_tool_item()
		configitem.set_size_request(80,50)
		self.toolbar.insert(configitem,-1)

		testitem=testaction.create_tool_item()
		testitem.set_size_request(80,50)
		self.toolbar.insert(testitem,-1)

		yunweiitem=yunweiaction.create_tool_item()
		yunweiitem.set_size_request(80,50)
		self.toolbar.insert(yunweiitem,-1)



		self.menubar=gtk.MenuBar()
		filem=gtk.MenuItem('文件')
		menu=gtk.Menu()
		exit=gtk.ImageMenuItem(gtk.STOCK_QUIT)
		exit.connect('activate',gtk.main_quit)
		menu.append(exit)
		filem.set_submenu(menu)
		self.menubar.append(filem)
		
		editm=gtk.MenuItem('编辑')
		menu=gtk.Menu()
		config=gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
		config.connect('activate',self.preferences)
		menu.append(config)
		editm.set_submenu(menu)
		self.menubar.append(editm)
		
		aboutm=gtk.MenuItem('关于')
		menu=gtk.Menu()
		about_me=gtk.MenuItem('关于作者')
		menu.append(about_me)
		about_she=gtk.MenuItem('关于软件')
		menu.append(about_she)
		aboutm.set_submenu(menu)
		self.menubar.append(aboutm)	

		helpm=gtk.MenuItem('帮助')
		menu=gtk.Menu()
		faq=gtk.MenuItem('FAQ')
		menu.append(faq)
		helpm.set_submenu(menu)
		self.menubar.append(helpm)
		self.vbox=gtk.VBox(False,0)
		self.vbox.pack_start(self.menubar,False,False,0)
		self.vbox.pack_start(self.toolbar,False,False,0)
		
		self.show_box=gtk.VBox(True,0)
		self.vbox.pack_start(self.show_box,True,True,0)

		#self.softbox=softcenter.SoftCenter().vbox
		self.softbox=softcenter.SoftCenter()
		self.show_box.pack_start(self.softbox,True,True,0)

		#self.deploybox=deploy.Deploy().vbox
		self.deploybox=deploy.DeployCenter()
		self.show_box.pack_start(self.deploybox,True,True,0)
		#self.set_focus(self.toolbar)

		self.configmanager=configmanager.ConfigManager()
		self.show_box.pack_start(self.configmanager,True,True,0)

		self.testcenter=testcenter.TestCenter()
		self.show_box.pack_start(self.testcenter,True,True,0)

		self.operationbox=operation.Operation()
		self.show_box.pack_start(self.operationbox,True,True,0)

		self.add(self.vbox)
		softaction.activate()
		self.menubar.show_all()
		self.toolbar.show()
		self.show_box.show()
		self.vbox.show()
		self.show()
	def switch(self,action,current):
		value=action.get_current_value()
		if (value == 0):
			self.soft_center()
		elif (value == 1):
			self.deploy_center()
		else:
			self._remove()
	def soft_center(self,action):
		self.show_box.hide_all()
		self.softbox.show_all()
		self.show_box.show()
		return
	def deploy_center(self,action):
		self.show_box.hide_all()
		self.deploybox.show_all()
		self.show_box.show()
		return	
		
	def config_center(self,action):
		self.show_box.hide_all()
		self.configmanager.show_all()
		self.show_box.show()
	def test_center(self,action):
		self.show_box.hide_all()
		self.testcenter.show_all()
		self.show_box.show()
	def yunwei_center(self,action):
		self.show_box.hide_all()
		self.operationbox.show_all()
		self.show_box.show()
	def update_center(self,action):
		pass
	#def _remove(self):
	#	children=self.show_box.get_children()
	#	if children is not None:
	#		for child in children:
	#			#self.show_box.remove(child)
	#			child.hide()
	#	#self.show_box.hide_all()
	def preferences(self,menuitem):
		b=gtk.Builder()
		b.add_from_file('xml/preferences.xml')
		w=b.get_object('mainwindow')
		w.set_position(gtk.WIN_POS_CENTER)
		w.show_all()
		
	def threads_init(self):
		gtk.gdk.threads_init()			
		
	def main(self):
                gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()

gospel=Gospel()
gospel.threads_init()
gospel.main()

