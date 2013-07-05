#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import threading
import sqlite3
import time
import paramiko

class SaveJdbcConfig(threading.Thread):
	def __init__(self,jdbc):
		self.serverlist=[]
		self.jdbc=jdbc
		threading.Thread.__init__(self)
	def run(self):
		#####show progress window#####
		progressWin=gtk.Window(gtk.WINDOW_TOPLEVEL)
		progressWin.set_size_request(600,50)
		progressWin.set_position(gtk.WIN_POS_CENTER)
		progressWin.set_keep_above(True)
		progressWin.set_decorated(False)
		vbox=gtk.VBox()
		vbox.set_border_width(5)
		progressWin.add(vbox)
		progressLabel=gtk.Label()
		vbox.add(progressLabel)
		progressBar=gtk.ProgressBar()
		progressBar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
		vbox.add(progressBar)
		progressWin.show_all()	
		#####start configing#####
		progressLabel.set_text('正在配置...')
		progressBar.set_fraction(0.1)
		progressBar.set_text('10%')
		progressLabel.set_text('正在获取孵化平台服务器列表...')
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute("select hostname from server where role='3'")
		data=cursor.fetchall()
		if data is not None:
			for host in data:
				self.serverlist.append(str(host[0]))	
		cursor.close()
		progressBar.set_fraction(0.3)
		progressBar.set_text('30%')
		progressLabel.set_text('正在配置JDBC...')
		if self.serverlist is not None:
			for host in self.serverlist:
				hostname=host
				####start config######
				conn=sqlite3.connect('db/server.db')
				cursor=conn.cursor()
				cursor.execute("select port,username,password from server where hostname='%s'"%hostname)
				data=cursor.fetchone()
				port=int(data[0])
				user=data[1]
				passwd=data[2]
				ssh=paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=hostname,port=port,username=user,password=passwd,timeout=60)
				ssh.exec_command("sed -i s'/[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/%s/' /opt/mkey3g/wwwroot/WEB-INF/classes/jdbc.properties"%self.jdbc)
		progressBar.set_fraction(1.0)
		progressBar.set_text('100%')
		progressLabel.set_text('配置完毕')
		time.sleep(1)
		progressWin.destroy()

class IncuBationConfig(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		self.set_border_width(20)

		self.fixed=gtk.Fixed()
		self.add(self.fixed)
		frame=gtk.Frame('JDBC连接配置')
		frame.set_size_request(810,140)
		self.fixed.put(frame,0,0)
		fixed=gtk.Fixed()
		frame.add(fixed)
		frame1=gtk.Frame('')
		frame1.set_size_request(700,110)
		fixed.put(frame1,50,0)
		fixed=gtk.Fixed()
		frame1.add(fixed)
		label=gtk.Label('JDBC地址')
		label.set_size_request(-1,-1)
		fixed.put(label,80,35)
		entry=gtk.Entry()
		entry.set_size_request(200,25)
		fixed.put(entry,140,30)
		button1=gtk.Button('高级选项')
		button1.set_size_request(100,25)
		fixed.put(button1,400,30)
		button2=gtk.Button('写入配置')
		button2.set_size_request(100,25)
		button2.connect('clicked',self.write_jdbc_config,entry)
		fixed.put(button2,520,30)
		button1.set_sensitive(False)
		button2.set_sensitive(False)
		entry.connect('insert-text',self.insert_text,[button1,button2])
		entry.connect('delete-text',self.delete_text,[button1,button2])
		
		self.fixed=gtk.Fixed()
		self.add(self.fixed)
		frame=gtk.Frame('双向同步配置')
		frame.set_size_request(810,140)
		self.fixed.put(frame,0,0)
		fixed=gtk.Fixed()
		frame.add(fixed)
		frame1=gtk.Frame('')
		frame1.set_size_request(700,110)
		fixed.put(frame1,50,0)
		fixed=gtk.Fixed()
		frame1.add(fixed)
		label=gtk.Label('同步目录')
		label.set_size_request(-1,-1)
		fixed.put(label,35,35)
		entry=gtk.Entry()
		entry.set_size_request(200,25)
		fixed.put(entry,140,30)
		button1=gtk.Button('高级选项')
		button1.set_size_request(100,25)
		fixed.put(button1,400,30)
		button2=gtk.Button('写入配置')
		button2.set_size_request(100,25)
		fixed.put(button2,520,30)
		button1.set_sensitive(False)
		button2.set_sensitive(False)
		entry.connect('insert-text',self.insert_text,[button1,button2])
		entry.connect('delete-text',self.delete_text,[button1,button2])
	def write_jdbc_config(self,widget,entry):
		jdbc=entry.get_text()
		T=SaveJdbcConfig(jdbc)
		T.setDaemon(True)
		T.start()
	def insert_text(self,entry,text,length,position,data):
                #print 'hhhh'
                data[0].set_sensitive(True)
                data[1].set_sensitive(True)
        def delete_text(self,entry,start,end,data):
                if start == 0:
                        data[0].set_sensitive(False)
                        data[1].set_sensitive(False)

