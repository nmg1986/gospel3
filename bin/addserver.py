#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import os
import variables
import sqlite3

class ShowAddWindow():
	def __init__(self,liststore):

		self.index=0
		self.liststore=liststore
		self.window=gtk.Window()
		self.window.set_keep_above(True)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_decorated(False)
		self.window.set_size_request(450,175)

		self.vbox=gtk.VBox()	
		self.window.add(self.vbox)

		self.vbox1=gtk.VBox()
		self.vbox.pack_start(self.vbox1,True,True,0)
		label=gtk.Label('添加服务器')
		self.vbox1.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.vbox1.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox1.pack_start(fixed,False,False,0)
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
		self.password.set_visibility(False)
		self.password.set_invisible_char('*')
		fixed.put(self.password,345,80)
		hline=gtk.HSeparator()
		hline.set_size_request(450,22)
		self.vbox1.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox1.pack_end(fixed,False,False,0)
		quitb=gtk.Button('退出')
		quitb.set_size_request(100,25)
		nextb=gtk.Button('下一步')
		nextb.set_size_request(100,25)
		quitb.connect('clicked',self.quit)
		nextb.connect('clicked',self.choose_role)
		fixed.put(quitb,5,5)
		fixed.put(nextb,345,5)
		
		self.vbox2=gtk.VBox()
		self.vbox.pack_start(self.vbox2,True,True,0)
		label=gtk.Label('选择角色')
		self.vbox2.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.vbox2.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox2.pack_start(fixed,False,False,0)
		self.radio1=gtk.RadioButton(None,'单机版MKEY',True)
		self.radio1.connect('clicked',self.mkey_toggled)
		
		fixed.put(self.radio1,5,5)
		self.radio2=gtk.RadioButton(self.radio1,'标准云平台',True)
		self.radio2.connect('toggled',self.cloud_toggled)
		#self.radio2.set_active(True)
		fixed.put(self.radio2,340,5)
		hline=gtk.HSeparator()
		self.vbox2.pack_start(hline,False,False,0)

		vbox=gtk.VBox()
		vbox.set_border_width(5)
		self.vbox2.pack_start(vbox,True,True,0)
		liststore=gtk.ListStore(str,str,bool)
		conn=sqlite3.connect('db/map.db')
		c=conn.cursor()
		c.execute('select * from map')
		while True:
			data=c.fetchone()
			if data is None:
				break
			index=str(data[0])
			name=str(data[1])
			liststore.append([name,index,False])
		conn.close()
		iter=liststore.get_iter_first()
		liststore.set_value(iter,2,True)
		self.roleview=gtk.TreeView(liststore)
		self.roleview.set_headers_visible(False)
		self.roleview.set_sensitive(False)
		selection=self.roleview.get_selection()
		selection.select_iter(iter)
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
		togglecell.set_property('activatable',True)
		#togglecell.set_activatable(True)
		togglecell.connect('toggled',self.toggled_role,self.roleview)
		togglecell.set_property('radio',False)
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
		self.vbox2.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox2.pack_start(fixed,False,False,0)
		returnb=gtk.Button('返回')
		nextb=gtk.Button('下一步')
		returnb.set_size_request(100,25)
		nextb.set_size_request(100,25)
		returnb.connect('clicked',self.return_1)
		nextb.connect('clicked',self.choose_soft)
		fixed.put(returnb,5,5)
		fixed.put(nextb,345,5)
		

		self.vbox3=gtk.VBox()
		self.vbox.pack_start(self.vbox3,True,True,0)
		label=gtk.Label('选择软件')
		self.vbox3.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.vbox3.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox3.pack_start(fixed,False,False,0)
		self.radio1=gtk.RadioButton(None,'默认软件包',True)
		self.radio1.connect('clicked',self.default_toggled)
		fixed.put(self.radio1,5,5)
		self.radio2=gtk.RadioButton(self.radio1,'自定义软件包',True)
		self.radio2.connect('toggled',self.custom_toggled)
		fixed.put(self.radio2,340,5)
		hline=gtk.HSeparator()
		self.vbox3.pack_start(hline,False,False,0)
		
		vbox=gtk.VBox()
		vbox.set_border_width(5)
		self.vbox3.pack_start(vbox,True,True,0)
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
		togglecell.connect('toggled',self.toggled_soft,self.softview)
		column=gtk.TreeViewColumn('选择',togglecell,active=1)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(100)
		self.softview.append_column(column)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
		sw.add(self.softview)
		vbox.pack_start(sw,True,True,0)
		hline=gtk.HSeparator()
		self.vbox3.pack_start(hline,False,False,0)
		fixed=gtk.Fixed()
		self.vbox3.pack_start(fixed,False,False,0)
		returnb=gtk.Button('返回')
		finishb=gtk.Button('完成')
		returnb.set_size_request(100,25)
		finishb.set_size_request(100,25)
		returnb.connect('clicked',self.return_2)
		finishb.connect('clicked',self.add_server)
		fixed.put(returnb,5,5)
		fixed.put(finishb,345,5)
		self.window.show_all()
		self.vbox2.hide()
		self.vbox3.hide()
	def toggled_role(self,cell,path,treeview):
		selection=treeview.get_selection()
		model,selected_path=selection.get_selected()
		if selected_path is not None:
			model[selected_path][2]=False
		model[path][2] = not model[path][2]
		selection.select_path(path)
		return
	def toggled_soft(self,cell,path,treeview):
		model=treeview.get_model()
		selection=treeview.get_selection()
		model[path][1] = not model[path][1]
		selection.select_path(path)
		return
	def default_toggled(self,radio):
		self.softview.set_sensitive(False)
	def custom_toggled(self,radio):
		self.softview.set_sensitive(True)
	def mkey_toggled(self,radio):
		self.roleview.set_sensitive(False)
	def cloud_toggled(self,radio):
		self.roleview.set_sensitive(True)
	def quit(self,widget):
		self.window.destroy()
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
		conn=sqlite3.connect('db/map.db')
		c=conn.cursor()
		c.execute("select package from map where id='%s'"%value)
		data=c.fetchone()
		pkg=str(data[0]).split(',')	
		model=self.softview.get_model()
		iter=model.get_iter_first()
		if iter is not None:
			model.set_value(iter,1,False)
			while True:
				iter=model.iter_next(iter)
				if iter is not None:
					model.set_value(iter,1,False)
				else:
					break
		iter=model.get_iter_first()
		if iter is not None:
			for item in pkg:
				while True:
					value=model.get_value(iter,0).split('-')[0]
					if item == value :
						model.set_value(iter,1,True)
						break
					else:
						iter=model.iter_next(iter)
						if iter is None:
							iter=model.get_iter_first()
		self.vbox3.show()
	def roleview_foreach(self,model,path,iter,data):
		for item in data:	
			print item
			value=model[path][0].split('-')[0]
			if item == value:
				model[path][1]=True
			else:
				model[path][1]=False
	def get_soft(self,model):
		pkg_list=[]
		iter=model.get_iter_first()
		if iter is not None:
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
					(hostname text,port text,username text,password text,role text,package text,type text,progress text,status text)
				'''
				)
		c.execute('''
					insert into server(hostname,port,username,password,role,package,type,progress,status)
					values("%s","%s","%s","%s","%s","%s","%s","%s","%s")
				  ''' % (data[0],data[1],data[2],data[3],data[4],data[5],'0','准备部署','0')
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
