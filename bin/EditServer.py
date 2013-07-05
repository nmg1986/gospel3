#!/usr/bin/python
#-*- coding:utf-8 -*-


import gtk
import sqlite3
import os

class EditServer():
	def __init__(self,host,index):
		self.host=host
		self.index=index
		self.conn=sqlite3.connect('db/server.db')
		c=self.conn.cursor()
		c.execute('''
					select port,username,password,package 
					from server 
					where hostname='%s' and role='%s'
				  '''%(self.host,self.index)
				)
		data=c.fetchone()
		self.port=str(data[0])
		self.username=str(data[1])
		self.password=str(data[2])	
		self.package=data[3].replace(' ','').replace('[','').replace(']','').replace("'","").split(',')

		w=gtk.Window()
		w.set_size_request(643,383)
		w.set_keep_above(True)
		w.set_position(gtk.WIN_POS_CENTER)
		vbox=gtk.VBox()
		w.add(vbox)
		label=gtk.Label('主机信息')
		label.set_size_request(300,25)
		label.set_width_chars(10)
		vbox.pack_start(label,False,False,0)

		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw,True,True,0)

		liststore=gtk.ListStore(str,str)
		treeview=gtk.TreeView(liststore)
		treeview.set_headers_visible(False)
		sw.add(treeview)
		
		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn('',text,text=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(320)
		treeview.append_column(column)

		text=gtk.CellRendererText()
		text.set_property('editable',True)
		column=gtk.TreeViewColumn('',text,text=1)
		treeview.append_column(column)

		liststore.append(['主机名',self.host])
		liststore.append(['端  口',self.port])
		liststore.append(['用户名',self.username])
		liststore.append(['密  码',self.password])

		label=gtk.Label('角色')
		label.set_size_request(200,25)
		label.set_width_chars(10)
		vbox.pack_start(label,False,False,0)

		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw,True,True,0)
		

		liststore=gtk.ListStore(bool,str,str)
		treeview=gtk.TreeView(liststore)
		treeview.set_headers_visible(False)
		sw.add(treeview)

		rendererToggle=gtk.CellRendererToggle()
		rendererToggle.set_activatable(True)
		rendererToggle.set_property('activatable',True)
		column=gtk.TreeViewColumn(' ',rendererToggle,active=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(20)
		column.set_resizable(True)
		treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("",rendererText,text=1)
		treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("Index",rendererText,text=2)
		column.set_visible(False)
		treeview.append_column(column)


		conn=sqlite3.connect('db/map.db')
		c=conn.cursor()
		c.execute('select name,id from map')
		while True:
			data=c.fetchone()
			if data is None:
				break
			name=str(data[0])
			id=str(data[1])
			if id == self.index: 
				liststore.append([True,name,id])
			liststore.append([False,name,id])
		conn.close()
		label=gtk.Label('软件包')
		label.set_size_request(200,25)
		label.set_width_chars(10)
		vbox.pack_start(label,False,False,0)

		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw,True,True,0)

		liststore=gtk.ListStore(bool,str)
		treeview=gtk.TreeView(liststore)
		treeview.set_headers_visible(False)
		sw.add(treeview)

		toggle=gtk.CellRendererToggle()
		toggle.set_property('xalign',0.5)
		column=gtk.TreeViewColumn('',toggle,active=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(20)
		treeview.append_column(column)

		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn("刷新",text,text=1)
		treeview.append_column(column)

		files=os.listdir('package')
		files.sort()
		for file in files:
			if file == 'list.server' or file == 'list.client':
				continue
			else:
				for package in self.package:
					if package == file.split('-')[0]:
						liststore.append([True,file])
						break
					else:
						continue
						
		w.show_all()
