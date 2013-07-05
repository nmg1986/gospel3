#!/usr/bin/python
# -*- coding:utf-8 -*-



import gtk

class Operation(gtk.HPaned):
	def __init__(self):
		gtk.HPaned.__init__(self)
		self.set_position(200)
	
		notebook=gtk.Notebook()
		self.vbox=gtk.VBox()
		label=gtk.Label('系统监控')
		self.add2(notebook)
		notebook.append_page(self.vbox,label)

		label=gtk.Label('检测项列表')
		label.set_size_request(-1,25)
		self.vbox.pack_start(label,False,False,0)
		hline=gtk.HSeparator()
		self.vbox.pack_start(hline,False,False,0)
		frame=gtk.Frame('平均负载(loadavg)检测')
		self.vbox.add(frame)
		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/loadavg.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)

		frame=gtk.Frame('CPU使用率检测')
		self.vbox.add(frame)

		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/cpu.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)
		

		frame=gtk.Frame('内存使用率检测')
		self.vbox.add(frame)

		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/memory.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)

		frame=gtk.Frame('磁盘使用率检测')
		self.vbox.add(frame)

		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/disk.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)
		#self.pack_start(vbox,True,True,0)


		frame=gtk.Frame('文件句柄检测')
		self.vbox.add(frame)
		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/loadavg.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)

		frame=gtk.Frame('Inode检测')
		self.vbox.add(frame)
		fixed=gtk.Fixed()
		frame.add(fixed)
		pixbuf=gtk.gdk.pixbuf_new_from_file_at_size('icon/loadavg.jpeg',50,50)
		image=gtk.Image()
		image.set_from_pixbuf(pixbuf)
		fixed.put(image,15,15)

		hbox=gtk.HBox()
		fixed=gtk.Fixed()
		button=gtk.Button('全部检测')
		button.set_size_request(100,25)
		fixed.put(button,0,0)
		hbox.pack_start(fixed,False,False,0)

		fixed=gtk.Fixed()
		button=gtk.Button('生成运维报告单')
		button.set_size_request(100,25)
		fixed.put(button,0,0)
		hbox.pack_end(fixed,False,False,0)

		self.vbox.pack_start(hbox,False,False,0)

		vbox=gtk.VBox()
		label=gtk.Label('数据备份')
		notebook.append_page(vbox,label)
		frame=gtk.Frame('目录备份')
		vbox.add(frame)
		frame=gtk.Frame('数据库备份')
		vbox.add(frame)

		vbox=gtk.VBox()
		label=gtk.Label('日志查看')
		notebook.append_page(vbox,label)
		#frame=gtk.Frame('在线查看')
		#vbox=gtk.VBox()
		#frame.add(vbox)
		#hbox=gtk.HBox()
		#fixed=gtk.Fixed()
		#hbox.pack_end(fixed,False,False,0)
		#button=gtk.Button('Tail -f')
		#button.set_size_request(100,25)
		#fixed.put(button,0,0)
		#vbox.add(hbox)
		#textview=gtk.TextView()
		#vbox.add(textview)
		#vbox.add(frame)
		#frame=gtk.Frame('远程抓取')
		#vbox.add(frame)

		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		
		treestore=gtk.TreeStore(str)
		treeview=gtk.TreeView(treestore)
		sw.add(treeview)
		#self.add1(sw)

		iter=treestore.append(None,['接入服务器'])
		treestore.append(iter,['192.168.1.10'])
		treestore.append(iter,['192.168.1.11'])

		iter=treestore.append(None,['中间件服务器'])
		treestore.append(iter,['192.168.1.12'])
		treestore.append(iter,['192.168.1.13'])
		treestore.append(iter,['192.168.1.14'])
		treestore.append(iter,['192.168.1.15'])

		iter=treestore.append(None,['管理平台'])
		treestore.append(iter,['192.168.1.16'])
		treestore.append(iter,['192.168.1.17'])

		iter=treestore.append(None,['孵化平台'])
		treestore.append(iter,['192.168.1.18'])
		treestore.append(iter,['192.168.1.19'])

		iter=treestore.append(None,['数据库服务器'])
		treestore.append(iter,['192.168.1.20'])
		treestore.append(iter,['192.168.1.21'])

		cell=gtk.CellRendererText()
		column=gtk.TreeViewColumn('服务器列表',cell,text=0)
		treeview.append_column(column)
if __name__ == '__main__':
	box=Operation()
	w=gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.set_size_request(1000,700)
	w.add(box)
	w.show_all()
	gtk.main()
