#!/usr/bin/python
# -*- coding:utf-8 -*- 
import gtk
from cellrendererbutton import *
from util import *
import download
import managesoftlist 
import variables
import multiprocessing
import addsoft

PKG_DIR='package'
class SoftCenter(gtk.VBox):
		def __init__(self):
			gtk.VBox.__init__(self)
			self.toolbar=gtk.Toolbar()
			self.toolbar.set_style(gtk.TOOLBAR_ICONS)
	
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
	
			addtb.connect("clicked",self.add_soft)
			deltb.connect("clicked",self.delete)
			cleartb.connect("clicked",self.clear)
			refresh.connect('clicked',self.refresh)
			prefer.connect('clicked',self.preference)
	
			self.pack_start(self.toolbar,False,False,0)
			self.liststore=gtk.ListStore(bool,str,str,str,str,str,str,int)
			self.treeview=gtk.TreeView(self.liststore)
			self.treeview.set_rules_hint(True)
			self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_NONE)
			self.treeview.set_fixed_height_mode(True)
			self.selection=self.treeview.get_selection()
			self.selection.set_mode(gtk.SELECTION_MULTIPLE)

			rendererToggle=gtk.CellRendererToggle()
			#rendererToggle.set_activatable(True)
			rendererToggle.set_property('activatable',True)
			rendererToggle.connect('toggled',self.toggled)
			column=gtk.TreeViewColumn(' ',rendererToggle,active=0)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			column.set_resizable(True)
			column.set_min_width(20)
			self.treeview.append_column(column)

			rendererText=gtk.CellRendererText()
			column=gtk.TreeViewColumn("软件包",rendererText,text=1)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			column.set_resizable(True)
			column.set_min_width(220)
			self.treeview.append_column(column)

			rendererText=gtk.CellRendererText()
			column=gtk.TreeViewColumn("功能描述",rendererText,text=2)
			column.set_min_width(250)
			column.set_resizable(True)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			self.treeview.append_column(column)

			rendererText=gtk.CellRendererText()
			column=gtk.TreeViewColumn("本地版本",rendererText,text=3)
			column.set_min_width(100)
			column.set_resizable(True)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			self.treeview.append_column(column)

			rendererText=gtk.CellRendererText()
			column=gtk.TreeViewColumn("最新版本",rendererText,text=4)
			column.set_min_width(100)
			column.set_resizable(True)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			self.treeview.append_column(column)

			rendererText=gtk.CellRendererText()
			column=gtk.TreeViewColumn("大小",rendererText,text=5)
			column.set_min_width(100)
			column.set_resizable(True)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			self.treeview.append_column(column)

			self.rendererButton=CellRendererButton()
			self.rendererButton.set_fixed_size(50,20)
			self.rendererButton.set_sensitive(False)
			self.rendererButton.connect('clicked',self.download_single)
			column=gtk.TreeViewColumn("状态",self.rendererButton,text=6,sensitive=7)
			column.set_alignment(0.5)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			column.set_resizable(True)
			column.set_min_width(50)
			self.treeview.append_column(column)

			self._init_model()
			self.pack_start(self.treeview,True,True,0)	
			hbox=gtk.HBox(False,3)
	
			fixed=gtk.Fixed()
			fixed.set_size_request(-1,25)
			self.choose_button=gtk.CheckButton("全部选中/反选")
			self.choose_button.connect('toggled',self.choose_all)
			fixed.put(self.choose_button,0,0)
			hbox.pack_start(fixed,False,False,0)
	
			fixed=gtk.Fixed()
			self.install_button=gtk.Button("下载/更新已选软件")
			self.install_button.set_size_request(120,25)
			self.install_button.connect('clicked',self.download_all)
			fixed.put(self.install_button,0,0)
			hbox.pack_end(fixed,False,False,0)
	
			self.pack_start(hbox,False,False,0)
		def fill_model(self,args):
			managesoftlist.ManageSoftList(args).get_soft_list()
		def _init_model(self): 			
			msl=managesoftlist.ManageSoftList(self.liststore)
			msl.get_soft_list()
		def flush_model(self):
			self.treeview.get_model().clear()
			self._init_model()
		def download_all(self,widget):
			selection=self.treeview.get_selection()
			model,paths = selection.get_selected_rows()
			if paths is not None:
				valid_path=[]
				for path in paths:
					treeiter=model.get_iter(path)	
					if model.get_value(treeiter,7) == 1:
						valid_path.append(path)
				variables.THREAD_NUM=len(valid_path)
				if len(valid_path) != 0:
					for path in valid_path:
						T=download.DownLoad(self.treeview,self.liststore,path)
						T.setDaemon(True)
						T.start()
					self.install_button.set_sensitive(False)
					self.choose_button.set_sensitive(False)
					W=download.WaitAll(self.install_button,self.choose_button,self.treeview)
					W.setDaemon(True)
					W.start()
		def download_single(self,widget,path):
				T=download.DownLoad(self.treeview,self.liststore,path)
				T.setDaemon(True)
				T.start()
		def choose_all(self,widget):
			if widget.get_active():
				self.treeview.get_selection().select_all()
				self.treeview.get_model().foreach(self.choose,True)
			else:	
				self.treeview.get_selection().unselect_all()
				self.treeview.get_model().foreach(self.choose,False)
		def choose(self,model,path,iter,data):
			model.set_value(iter,0,data)

		def start_update(self,widget):
			pass
			
		def toggled(self,cell,path):
			model=self.treeview.get_model()
			model[path][0]= not model[path][0]	
			self.selection.unselect_path(path)
		#def destroy(self,widget):
		#	widget.destroy()
		#def main(self):
		#	gtk.main()
		
		def select_changed(self,selection):
			model,paths = selection.get_selected_rows()
			if paths is not None:
				for path in paths:
					treeiter=model.get_iter(path)
					value=not self.liststore.get_value(treeiter,0)
					self.liststore.set_value(treeiter,0,value)
			#self.choose_button.set_active(True)
		def add_soft(self,widget):
			w=addsoft.AddSoft(self.liststore)
			w.show()
		def delete(self,widget):
			model,paths=self.selection.get_selected_rows()
			if paths is not None:
				for path in paths:
					iter=self.liststore.get_iter(path)
					self.liststore.remove(iter)
			return
		def clear(self,widget):
			self.liststore.clear()
			return
		def refresh(self,widget):
			self.liststore.clear()
			managesoftlist.ManageSoftList(self.liststore).get_soft_list()
			return
		def preference(self,widget):
			b=gtk.Builder()
			b.add_from_file('xml/preferences.xml')
			w=b.get_object('mainwindow')
			w.set_keep_above(True)
			w.set_position(gtk.WIN_POS_CENTER)
			button=b.get_object('button1')
			button.connect('clicked',self.save_config,w)
			w.show_all()
		def save_config(self,widget,data):
			data.destroy()	
			
					
if __name__ == '__main__':
	box=SoftCenter()
	w=gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.set_size_request(1000,700)
	w.add(box)
	w.show_all()
	gtk.main()
	
#app=Upgrade()
#app.main()
