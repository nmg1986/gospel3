#!/usr/bin/python
#-*- coding:utf-8 -*-


import gtk

class ServerPool(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)

		toolbar=gtk.Toolbar()
		toolbar.set_style(gtk.TOOLBAR_ICONS)
	
		addtb=gtk.ToolButton(gtk.STOCK_ADD)
		addtb.set_tooltip_text('添加')
		deltb=gtk.ToolButton(gtk.STOCK_REMOVE)
		deltb.set_tooltip_text('删除')
		cleartb=gtk.ToolButton(gtk.STOCK_CLEAR)
		cleartb.set_tooltip_text('清空列表')
		refresh=gtk.ToolButton(gtk.STOCK_REFRESH)
		refresh.set_tooltip_text('刷新')
	       
		toolbar.insert(addtb,0)
		toolbar.insert(deltb,1)
		toolbar.insert(cleartb,2)
		toolbar.insert(refresh,3)
	
		addtb.connect("clicked",self.add_server)
		deltb.connect("clicked",self.delete_server)
		cleartb.connect("clicked",self.clear_server)
	
		self.pack_start(toolbar,False,False,0)

		self.hpaned=gtk.HPaned()
		self.hpaned.set_position(150)	
		self.pack_start(self.hpaned,True,True,0)

		sw=gtk.ScrolledWindow()
		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		self.hpaned.add1(sw)

		self.pixbuf_large=gtk.gdk.pixbuf_new_from_file_at_size('icon/server.png',60,60)
		self.pixbuf_small=gtk.gdk.pixbuf_new_from_file_at_size('icon/server.png',20,20)

		store=gtk.ListStore(str,gtk.gdk.Pixbuf)
		self.iconview=gtk.IconView(store)
		self.iconview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,[('text/plain',0,0)],gtk.gdk.ACTION_COPY)
		self.iconview.connect('drag-data-get',self.drag_data_get)
		self.iconview.set_text_column(0)
		self.iconview.set_pixbuf_column(1)
		sw.add(self.iconview)
		store.append(['单机版MKEY',self.pixbuf_large])
		store.append(['接入服务器',self.pixbuf_large])
		store.append(['中间件服务器',self.pixbuf_large])
		store.append(['管理平台',self.pixbuf_large])
		store.append(['孵化平台',self.pixbuf_large])
		store.append(['数据库服务器',self.pixbuf_large])
		store.append(['MFS管理服务器',self.pixbuf_large])
		store.append(['MFS备份服务器',self.pixbuf_large])
		store.append(['MFS存储服务器',self.pixbuf_large])
		store.append(['MFS客户端',self.pixbuf_large])

		

		self.vbox=gtk.VBox()
		self.hpaned.add2(self.vbox)

		sw=gtk.ScrolledWindow()
		sw=gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		self.vbox.add(sw)

		self.liststore=gtk.ListStore(str,str,str,str,str,gtk.gdk.Pixbuf)
		self.treeview=gtk.TreeView(self.liststore)
		self.treeview.enable_model_drag_dest([('text/plain',0,0)],gtk.gdk.ACTION_COPY)
		#treeview.drag_dest_set(gtk.DEST_DEFAULT_ALL,[('text/plain',0,0)],gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
		self.treeview.connect('drag-data-received',self.drag_data_received)
		sw.add(self.treeview)

		rendererPixbuf=gtk.CellRendererPixbuf()
		column=gtk.TreeViewColumn('',rendererPixbuf,pixbuf=5)	
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(30)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("角色",rendererText,text=0)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(135)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.connect('edited',self.edited,1)
		rendererText.set_property('editable',True)
		column=gtk.TreeViewColumn("服务器IP",rendererText,text=1)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(170)
		self.treeview.append_column(column)
		
		rendererText=gtk.CellRendererText()
		rendererText.set_property('editable',True)
		rendererText.connect('edited',self.edited,2)
		column=gtk.TreeViewColumn("端口",rendererText,text=2)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(105)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.set_property('editable',True)
		rendererText.connect('edited',self.edited,3)
		column=gtk.TreeViewColumn("用户名",rendererText,text=3)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(110)
		self.treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.set_property('editable',True)
		rendererText.connect('edited',self.edited,4)
		column=gtk.TreeViewColumn("密码",rendererText,text=4)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(92)
		self.treeview.append_column(column)

	def add_server(self,widget):
		selected_path=self.iconview.get_selected_items()[0]
		selected_iter=self.iconview.get_model().get_iter(selected_path)
		text=self.iconview.get_model().get_value(selected_iter,0)
		self.liststore.append([text,'--','--','--','--',self.pixbuf_small])
	def delete_server(self,widget):
		selection=self.treeview.get_selection()
		model,iter = selection.get_selected()
		if iter is not None:
			model.remove(iter)
	def clear_server(self,widget):
		model=self.treeview.get_model()
		model.clear()
	def edited(self,cell,path,text,column):
		self.liststore[path][column]=text
		if column == 4:
			iter=self.liststore.get_iter(path)
			value=self.liststore.get_value(iter,0)
			print value
	def drag_data_received(self,widget,drag_context,x,y,data,info,time):
		#if info == 0:
		text=data.get_text()
		text = text.decode('unicode_escape')
		self.liststore.append([text,'--','--','--','--',self.pixbuf_small])
	def drag_data_get(self,widget,drag_context,data,info,time):
		selected_path=widget.get_selected_items()[0]
		selected_iter=widget.get_model().get_iter(selected_path)
		if info == 0:
			text=widget.get_model().get_value(selected_iter,0)
			data.set_text(text,-1)
		elif info == 0:
			pixbuf=widget.get_model().get_value(selected_iter,1)
			data.set_pixbuf(pixbuf)
