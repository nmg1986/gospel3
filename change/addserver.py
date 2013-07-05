#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import os
import variables
import sqlite3

class HostInfo(gtk.VBox):
		def __init__(self):
			gtk.VBox.__init__(self)
				
			label=gtk.Label('添加服务器')
			self.pack_start(label,False,False,0)
			hline=gtk.HSeparator()
			self.pack_start(hline,False,False,0)
			fixed=gtk.Fixed()
			self.pack_start(fixed,False,False,0)
			label=gtk.Label('主机IP')
			fixed.put(label,5,5)
			label=gtk.Label('端口')
			fixed.put(label,345,5)
			self.hostname=gtk.Entry()
			self.hostname.set_size_request(180,25)
			fixed.put(self.hostname,5,25)
			self.port=gtk.Entry()
			self.port.set_size_request(100,25)
			fixed.put(self.port,345,25)
			label=gtk.Label('用户名')
			fixed.put(label,5,60)
			label=gtk.Label('密码')
			fixed.put(label,345,60)
			self.username=gtk.Entry()
			self.username.set_size_request(120,25)
			fixed.put(self.username,5,80)
			self.password=gtk.Entry()
			self.password.set_size_request(100,25)
			fixed.put(self.password,345,80)
			hline=gtk.HSeparator()
			hline.set_size_request(450,22)
			self.pack_start(hline,False,False,0)
			fixed=gtk.Fixed()
			self.pack_end(fixed,False,False,0)
			quitb=gtk.Button('退出')
			quitb.set_size_request(100,25)
			nextb=gtk.Button('下一步')
			nextb.set_size_request(100,25)
			quitb.connect('clicked',self.quit)
			nextb.connect('clicked',self.choose_role)
			fixed.put(quitb,5,5)
			fixed.put(nextb,345,5)
		def quit(self,widget):
			self.window.destroy()
		def show(self):
			self.show_all()
		def hide(self):
			self.hide_all()

class RoleInfo(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		
		label=gtk.Label('选择角色')
		self.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.pack_start(hline,False,False,0)
		vbox=gtk.VBox()
		vbox.set_border_width(5)
		self.pack_start(vbox,True,True,0)
		liststore=gtk.ListStore(str,str,bool)
		liststore.append(['接入服务器',0,False])	
		liststore.append(['中间件服务器',1,False])	
		liststore.append(['云管理平台',2,False])	
		liststore.append(['云孵化平台',3,False])	
		liststore.append(['云应用门户',4,False])	
		liststore.append(['数据库服务器',5,False])	
		self.roleview=gtk.TreeView(liststore)
		self.roleview.set_headers_visible(False)
		textcell=gtk.CellRendererText()
		column=gtk.TreeViewColumn('角色列表',textcell,text=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(350)
		self.roleview.append_column(column)
		textcell=gtk.CellRendererText()
		column=gtk.TreeViewColumn('Index',textcell,text=1)
		column.set_visible(False)
		self.roleview.append_column(column)
		togglecell=gtk.CellRendererToggle()
		togglecell.set_activatable(True)
		togglecell.connect('toggled',self.toggled,self.roleview)
		togglecell.set_property('radio',True)
		togglecell.set_property('xalign',0.5)
		togglecell.set_property('yalign',0.5)
		column=gtk.TreeViewColumn('选择',togglecell,active=2)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(100)
		self.roleview.append_column(column)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
		sw.add(self.roleview)
		vbox.pack_start(sw,True,True,0)
		hline=gtk.HSeparator()
		self.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.pack_start(fixed,False,False,0)
		returnb=gtk.Button('返回')
		nextb=gtk.Button('下一步')
		returnb.set_size_request(100,25)
		nextb.set_size_request(100,25)
		returnb.connect('clicked',self.return_1)
		nextb.connect('clicked',self.choose_soft)
		fixed.put(returnb,5,5)
		fixed.put(nextb,345,5)
	def toggled(self,cell,path,treeview):
		selection=treeview.get_selection()
		model,selected_path=selection.get_selected()
		if selected_path is not None:
			model[selected_path][2]=False
		model[path][2] = not model[path][2]
		return
	def show(self):
		self.show_all()
	def hide(self):
		self.hide_all()
		
class SoftInfo(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)	
		label=gtk.Label('选择软件')
		self.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.pack_start(fixed,False,False,0)
		self.radio1=gtk.RadioButton(None,'默认软件包',True)
		self.radio1.connect('clicked',self.default_toggled)
		fixed.put(self.radio1,5,5)
		self.radio2=gtk.RadioButton(self.radio1,'自定义软件包',True)
		self.radio2.connect('toggled',self.custom_toggled)
		fixed.put(self.radio2,340,5)
		hline=gtk.HSeparator()
		self.pack_start(hline,False,False,0)
		
		vbox=gtk.VBox()
		vbox.set_border_width(5)
		self.pack_start(vbox,True,True,0)
		liststore=gtk.ListStore(str,bool)
		files=os.listdir('package')
		files.sort()
		for file in files:
			if file == 'list.server' or file == 'list.client':
				continue
			else:
				liststore.append([file,False])
		self.softview=gtk.TreeView(liststore)
		self.softview.set_headers_visible(False)
		self.softview.set_sensitive(False)
		selection=self.softview.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
		textcell=gtk.CellRendererText()
		column=gtk.TreeViewColumn('软件列表',textcell,text=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(350)
		self.softview.append_column(column)
		togglecell=gtk.CellRendererToggle()
		togglecell.connect('toggled',self.toggled,self.softview)
		column=gtk.TreeViewColumn('选择',togglecell,active=1)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(100)
		self.softview.append_column(column)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
		sw.add(self.softview)
		vbox.pack_start(sw,True,True,0)
		hline=gtk.HSeparator()
		self.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.pack_start(fixed,False,False,0)
		returnb=gtk.Button('返回')
		finishb=gtk.Button('完成')
		returnb.set_size_request(100,25)
		finishb.set_size_request(100,25)
		returnb.connect('clicked',self.return_2)
		finishb.connect('clicked',self.add_server)
		fixed.put(returnb,5,5)
		fixed.put(finishb,345,5)
	def toggled(self,cell,path,treeview):
		model=treeview.get_model()
		selection=treeview.get_selection()
		model[path][1] = not model[path][1]
		selection.select_path(path)
	def default_toggled(self,radio):
		self.softview.set_sensitive(False)
	def custom_toggled(self,radio):
		self.softview.set_sensitive(True)
		return
	def show(self):
		self.show_all()
	def hide(self):
		self.hide_all()

class ShowAddWindow():
	def __init__(self,liststore):

		self.liststore=liststore
		self.window=gtk.Window()
		self.window.set_keep_above(True)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_decorated(False)
		self.window.set_size_request(450,175)

		self.vbox=gtk.VBox()	
		self.window.add(self.vbox)

		self.vbox1=HostInfo()
		self.vbox2=RoleInfo()
		self.vbox3=SoftInfo()

		self.vbox.pack_start(self.vbox1,True,True,0)
		self.vbox.pack_start(self.vbox2,True,True,0)
		self.vbox.pack_start(self.vbox3,True,True,0)
		
		self.vbox1.show()
		self.vbox2.hide()
		self.vbox3.hide()
		self.window.show()
	def choose_role(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()
		self.vbox1.hide()
		self.vbox2.show()
	def choose_soft(self,widget):
		self.vbox2.hide()
		selection=self.roleview.get_selection()
		model,path=selection.get_selected()
		value=model[path][1]
		pkg=variables.PKG_DIC[value]
		self.softview.get_model().foreach(self.roleview_foreach,pkg)
		self.vbox3.show()
	def roleview_foreach(self,model,path,iter,data):
		for item in data.split(','):	
			value=model[path][0].split('-')[0]
			if item == value:
				model[path][1]=True
	def get_soft(self,model):
		pkg_list=[]
		iter=model.get_iter_first()
		if model.get_value(iter,1):
			pkg_list.append(model.get_value(iter,0))
		while model.iter_next(iter) is not None:
			iter=model.iter_next(iter)
			if model.get_value(iter,1):
				pkg_list.append(model.get_value(iter,0))
		return pkg_list
	def return_1(self,widget):
		self.vbox2.hide()
		self.vbox1.show()
	def return_2(self,widget):
		self.vbox3.hide()
		self.vbox2.show()
	def add_server(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()
		selection=self.roleview.get_selection()
		model,path=selection.get_selected()
		if path is not None:	
			role=model[path][0]
			index=model[path][1]
		if self.radio1.get_active():
			soft=self.radio1.get_label()
			flag=0
		else:
			soft=self.radio2.get_label()
			flag=1
		model=self.softview.get_model()
		pkg_list=[]
		pkg_list=self.get_soft(model)
		self.saveTodb([hostname,port,username,password,index,pkg_list])
		self.liststore.append([False,hostname,role,index,soft,flag,'准备部署','--'])
		self.window.destroy()
	def saveTodb(self,data):
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
					create table if not exists server
					(hostname text,port text,username text,password text,role text,package text)
				'''
				)
		c.execute('''
					insert into server(hostname,port,username,password,role,package)
					values("%s","%s","%s","%s","%s","%s")
				  ''' % (data[0],data[1],data[2],data[3],data[4],data[5])
				)
		conn.commit()
		conn.close()
	def msg(self,text):
		md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,
								gtk.BUTTONS_OK,text)
		md.run()
		md.destroy()
	def IsValid(self,text):
		list=text.split('.')
		if len(list) != 4 :
			return False
		else:
			for i in list:
				if i.isdigit() and 0 <= int(i) <= 255:
					continue
				else:
					return False
		return True
