#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import os

class AddSoft:
	def __init__(self,model):
		b=gtk.Builder()
		b.add_from_file('xml/addsoft.xml')
		self.f=b.get_object('filechooserdialog')
		self.f.set_position(gtk.WIN_POS_CENTER)
		self.f.set_keep_above(True)
		
		textview=b.get_object('textview')
		textbuffer=gtk.TextBuffer()
		textview.set_buffer(textbuffer)

		add=b.get_object('add')
		quit=b.get_object('quit')
		
		add.connect('clicked',self.add,textbuffer)
		quit.connect('clicked',self.quit)
		self.liststore=model
	def show(self):
		self.f.show_all()
	def quit(self,widget):
		self.f.destroy()
	def add(self,widget,buffer):
		filepath=self.f.get_filename()
		filename=os.path.basename(filepath)
		name=filename.split('-')[0]
		version=filename.split('-')[1].split('.tar')[0]
		start,end=buffer.get_bounds()
		text=buffer.get_text(start,end,False)
		size=os.path.getsize(filepath)/1024
		size=str(size)+'M'
		
		self.liststore.append([False,name,text,version,version,size,'最新',0])	
		self.f.destroy()
