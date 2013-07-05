#!/usr/bin/python
# -*- coding:utf-8 -*-
	 
import gtk
from addserver import *
import util
import os
import sqlite3
import EditServer

DEFAULT=0
CUSTOM=1 

class DeployCenter(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)	

		self.toolbar=gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_ICONS)
		self.pack_start(self.toolbar,False,False,0)
	
		addtb=gtk.ToolButton(gtk.STOCK_ADD)
		addtb.set_tooltip_text('添加')
		deltb=gtk.ToolButton(gtk.STOCK_REMOVE)
		deltb.set_tooltip_text('删除')
		cleartb=gtk.ToolButton(gtk.STOCK_CLEAR)
		cleartb.set_tooltip_text('清空列表')
		refresh=gtk.ToolButton(gtk.STOCK_REFRESH)
		refresh.set_tooltip_text('刷新')
		info=gtk.ToolButton(gtk.STOCK_INFO)
		info.set_tooltip_text('日志')
		edit=gtk.ToolButton(gtk.STOCK_EDIT)
		edit.set_tooltip_text('编辑')
		prefer=gtk.ToolButton(gtk.STOCK_PREFERENCES)
		prefer.set_tooltip_text('配置')
	       
		self.toolbar.insert(addtb,0)
		self.toolbar.insert(deltb,1)
		self.toolbar.insert(cleartb,2)
		self.toolbar.insert(refresh,3)
		self.toolbar.insert(info,4)
		self.toolbar.insert(edit,5)
		self.toolbar.insert(prefer,6)
	
		addtb.connect("clicked",self.add_server)
		deltb.connect("clicked",self.delete)
		cleartb.connect("clicked",self.clear)
		edit.connect('clicked',self.edit)
		prefer.connect('clicked',self.preference)
	
		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		self.pack_start(sw,True,True,0)
	
		#self.liststore=gtk.ListStore(bool,str,str,str,str,str,str,str)
		self.liststore=self.create_model()
		self.treeview=gtk.TreeView(self.liststore)
		self.selection=self.treeview.get_selection()
		self.selection.set_mode(gtk.SELECTION_MULTIPLE)
		sw.add(self.treeview)
	
		rendererToggle=gtk.CellRendererToggle()
		rendererToggle.set_activatable(True)
		rendererToggle.connect('toggled',self.toggled,self.treeview)
		column=gtk.TreeViewColumn(' ',rendererToggle,active=0)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(25)
		self.treeview.append_column(column)
	
		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("服务器",rendererText,text=1)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(160)
		self.treeview.append_column(column)
	
		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("角色",rendererText,text=2)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(236)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("Index",rendererText,text=3)
		column.set_visible(False)
		self.treeview.append_column(column)
	
		rendererText=gtk.CellRendererCombo()
		column=gtk.TreeViewColumn("软件包",rendererText,text=4)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(True)
		column.set_fixed_width(178)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("Flag",rendererText,text=5)
		column.set_visible(False)
		self.treeview.append_column(column)
	
		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("部署进度",rendererText,text=6)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(True)
		column.set_fixed_width(210)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("状态",rendererText,text=7)
		column.set_visible(True)
		self.treeview.append_column(column)


		self.hbox=gtk.HBox(False,3)
		self.pack_start(self.hbox,False,False,0)
		fixed=gtk.Fixed()
		fixed.set_size_request(-1,25)
		self.choose_button=gtk.CheckButton("全部选中/反选")
		self.choose_button.connect('toggled',self.choose_all)
		fixed.put(self.choose_button,0,0)
		self.hbox.pack_start(fixed,False,False,0)

	
		fixed=gtk.Fixed()
		self.install_button=gtk.Button("开始部署")
		self.install_button.set_size_request(100,25)
		self.install_button.connect('clicked',self.start_install)
		fixed.put(self.install_button,0,0)
		self.hbox.pack_end(fixed,False,False,0)
	def create_model(self):
		liststore=gtk.ListStore(bool,str,str,str,str,str,str,str)
		if os.path.isfile('db/server.db'):
			conn=sqlite3.connect('db/server.db')
			cursor=conn.cursor()
			cursor.execute('select hostname,role,type,progress,status from server') 
			while True:
				data=cursor.fetchone()
				if data is None:
					break
				hostname=str(data[0])
				index=str(data[1])
				_conn=sqlite3.connect('db/map.db')
				_cursor=_conn.cursor()
				_cursor.execute("select name from map where id='%s'"%index)
				_data=_cursor.fetchone()
				role=str(_data[0])
				flag=str(data[2])
				if flag == '0':
					soft='默认软件包'
				else:
					soft='自定义软件包'
				progress=str(data[3])
				status=str(data[4])	
				if status == '0':
					status='--'
				else:
					status='√' 
				liststore.append([False,hostname,role,index,soft,flag,progress,status])
			#_cursor.close()
			#_conn.close()
			cursor.close()
			conn.close()
		return liststore
				

	def toggled(self,cell,path,treeview):
		model=treeview.get_model()
		model[path][0] = not model[path][0]
		self.selection.select_path(path)
		return
	def add_server(self,widget):
		win=ShowAddWindow(self.liststore)
		return
	def destroy_add(self,widget,data):
		data.destroy()
		return
	def start_install(self,widget):
		selection=self.treeview.get_selection()
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				treeiter=model.get_iter(path)
				T=util.INSTALL(model,treeiter,self.liststore)
				T.setDaemon(True)
				T.start()
		return
	def delete(self,widget):
		selection=self.treeview.get_selection()
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				host=model[path][1]
				role=model[path][3]
				conn=sqlite3.connect('db/server.db')	
				c=conn.cursor()
				c.execute("delete from server where hostname='%s' and role='%s'"%(host,role))
				conn.commit()
				conn.close()
				model.remove(model.get_iter(path))		
		return
	def clear(self,widget):
		self.liststore.clear()
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('delete from server')
		conn.commit()
		conn.close()
		return	
	def choose_all(self,widget):
		if widget.get_active():
			self.treeview.get_selection().select_all()
			self.treeview.get_model().foreach(self.choose,True)
		else:	
			self.treeview.get_selection().unselect_all()
			self.treeview.get_model().foreach(self.choose,False)
		return
	def choose(self,model,path,iter,data):
		model.set_value(iter,0,data)
		return
	def select_changed(self,selection):
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				treeiter=model.get_iter(path)
				value=not self.liststore.get_value(treeiter,0)
				self.liststore.set_value(treeiter,0,value)
		return
	def edit(self,widget):
		selection=self.treeview.get_selection()
		model,paths=selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				host=model[path][1]
				index=model[path][3]
			EditServer.EditServer(host,index)

	def preference(self,widget):
		b=gtk.Builder()
		b.add_from_file('xml/softpreference.xml')
		w=b.get_object('mainwindow')
		w.set_size_request(600,460)
		w.set_keep_above(True)
		w.set_position(gtk.WIN_POS_CENTER)
		hpaned=b.get_object('hpaned1')
		hpaned.set_position(150)
		treeview1=b.get_object('treeview1')
		model=gtk.ListStore(str,int)
		model.append(['接入服务器',0])
		model.append(['云中间件',1])
		model.append(['云管理平台',2])
		model.append(['云孵化平台',3])
		model.append(['数据库服务器',4])
		model.append(['双机热备',5])
		model.append(['MFS主控服务器',6])
		model.append(['MFS备份服务器',7])
		model.append(['MFS数据服务器',8])
		model.append(['MFS客户端服务器',9])
		treeview1.set_model(model)
		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn('角色列表',text,text=0)
		treeview1.append_column(column)

		model=gtk.ListStore(bool,str)
		files=os.listdir('package')
		files.sort()
		for file in files:
			if file == 'list.server' or file == 'list.client':
				continue
			else:
				model.append([False,file])
		treeview2=b.get_object('treeview2')
		treeview2.set_model(model)
		toggle=gtk.CellRendererToggle()
		column=gtk.TreeViewColumn('',toggle,active=0)
		treeview2.append_column(column)
		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn('软件包列表',text,text=1)
		treeview2.append_column(column)
		button=b.get_object('button1')	
		button.connect('clicked',self.save_config,w)	
		
		w.show_all()
		return 
	def save_config(self,widget,data):
		data.destroy()	
		

if __name__ == "__main__":
	box=Deploy()
	w=gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.set_size_request(1000,700)
	w.add(box)
	w.show_all()
	gtk.main()
