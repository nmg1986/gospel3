#!/usr/bin/python
#-*- coding:utf-8 -*-

import gtk
import threading
import sqlite3
import time
import paramiko
import os

class SaveHAConfig(threading.Thread):
	def __init__(self,master,slave,vip):
		self.master=master
		self.slave=slave
		self.vip=vip

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
		#####get master info#####	
		progressLabel.set_text('正在获取主机信息...')
		progressBar.set_fraction(0.0)
		progressBar.set_text('0%')
		progressBar.set_fraction(0.1)
		progressBar.set_text('10%')
		self.conn=sqlite3.connect('db/server.db')
		cursor=self.conn.cursor()
		cursor.execute("select port,username,password from server where hostname='%s'"%self.master)
		data=cursor.fetchone()
		mport=int(data[0])
		muser=data[1]
		mpasswd=data[2]
		print self.master,mport,muser,mpasswd
		#####get slave info#####
		progressLabel.set_text('正在获取备机信息...')
		progressBar.set_fraction(0.2)
		progressBar.set_text('20%')
		cursor.execute("select port,username,password from server where hostname='%s'"%self.slave)
		data=cursor.fetchone()
		sport=int(data[0])
		suser=data[1]
		spasswd=data[2]
		cursor.close()
		self.conn.close()
		print self.slave,sport,suser,spasswd
		#####get nic and gateway#####
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.master,port=mport,username=muser,password=mpasswd,timeout=60)
		#######get nic########
		progressLabel.set_text('正在获取网卡信息...')
		progressBar.set_fraction(0.4)
		progressBar.set_text('40%')
		stdin,stdout,stderr=ssh.exec_command('ifconfig -a | grep  HWaddr|grep -v lo')
		nic=stdout.readlines()[-1].split(' ')[0]
		print nic
		#######get gateway######
		progressLabel.set_text('正在获取网关信息...')
		progressBar.set_fraction(0.6)
		progressBar.set_text('60%')
		stdin,stdout,stderr=ssh.exec_command("cat /etc/sysconfig/network/routes | awk '{print $2}'")
		gateway=stdout.readlines()[0]
		print gateway
		ssh.close()
		#####start master config######
		progressLabel.set_text('正在配置主机...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.master,port=mport,username=muser,password=mpasswd,timeout=60)
		ssh.exec_command('echo nginx-master > /etc/HOSTNAME')
		ssh.exec_command("hostname nginx-master")
		ssh.exec_command("/usr/bin/sed -i '/^bcast/cbcast %s' /etc/ha.d/ha.cf" % nic)
		ssh.exec_command("/usr/bin/sed -i '/^node/,+1 c node nginx-master\\nnode nginx-slave' /etc/ha.d/ha.cf")
		ssh.exec_command("/usr/bin/sed -i '/^ping/cping %s' /etc/ha.d/ha.cf" % gateway)
		ssh.exec_command("echo nginx-master IPaddr::%s tomcat > /etc/ha.d/haresources" % self.vip)
		progressLabel.set_text('正在配置进程监控...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("/usr/bin/sed -i '/^#\[tomcat\]/,+2 s/^#//'     /etc/solomon.conf")
		progressLabel.set_text('正在配置邮件告警...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("/usr/bin/sed -i '/^host=/chost=%s' /etc/solomon/conf.d/email.conf" % self.master)

		
		
		
		#####start slave config#####
		progressLabel.set_text('正在配置备机...')
		progressBar.set_fraction(0.9)
		progressBar.set_text('90%')
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.slave,port=sport,username=suser,password=spasswd,timeout=60)
		ssh.exec_command('echo nginx-slave > /etc/HOSTNAME')
		ssh.exec_command("hostname nginx-slave")
		ssh.exec_command("sed -i '/^bcast/cbcast %s' /etc/ha.d/ha.cf" % nic)
		ssh.exec_command("sed -i '/^node/,+1 cnode nginx-master\\nnode nginx-slave' /etc/ha.d/ha.cf")
		ssh.exec_command("sed -i '/^ping/cping %s' /etc/ha.d/ha.cf" % gateway)
		ssh.exec_command("echo nginx-master IPaddr::%s tomcat > /etc/ha.d/haresources" % self.vip)
		progressLabel.set_text('正在配置进程监控...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("sed -i '/^#\[tomcat\]/,+2 s/^#//'     /etc/solomon.conf")
		progressLabel.set_text('正在配置邮件告警...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("sed -i '/^host=/chost=%s' /etc/solomon/conf.d/email.conf" % self.master)
		#####close ssh connection#####
		ssh.close()
		#####config finished#####
		progressLabel.set_text('配置完毕')
		progressBar.set_fraction(1.0)
		progressBar.set_text('100%')
		time.sleep(1)
		progressWin.destroy()

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
		progressLabel.set_text('正在获取应用门户服务器列表...')
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute("select hostname from server where role='4'")
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


class AppPortalConfig(gtk.VBox):
	def __init__(self):
		self.index=4

		gtk.VBox.__init__(self)
		self.set_border_width(20)
		self.connect('expose-event',self._expose)

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
		button2=gtk.Button('一键配置')
		button2.set_size_request(100,25)
		button2.connect('clicked',self.write_jdbc_config,entry)
		fixed.put(button2,520,30)
		button1.set_sensitive(False)
		button2.set_sensitive(False)
		entry.connect('insert-text',self.insert_text,[button1,button2])
		entry.connect('delete-text',self.delete_text,[button1,button2])

		self.fixed=gtk.Fixed()
		self.add(self.fixed)
		frame=gtk.Frame('HA双机配置')
		frame.set_size_request(810,140)
		self.fixed.put(frame,0,0)
		fixed=gtk.Fixed()
		frame.add(fixed)
		frame1=gtk.Frame('')
		frame1.set_size_request(700,110)
		fixed.put(frame1,50,0)
		fixed=gtk.Fixed()
		frame1.add(fixed)
		label=gtk.Label('主机')
		label.set_size_request(-1,-1)
		fixed.put(label,100,0)
		self.combox1=gtk.ComboBoxEntry()
		self.combox1.set_text_column(0)
		self.combox1.set_size_request(150,25)
		fixed.put(self.combox1,100,17)
		label=gtk.Label('备机')
		label.set_size_request(-1,-1)
		fixed.put(label,310,0)
		self.combox2=gtk.ComboBoxEntry()
		self.combox2.set_text_column(0)
		self.combox2.set_size_request(150,25)
		fixed.put(self.combox2,310,17)
		label=gtk.Label('虚IP')
		label.set_size_request(-1,-1)
		fixed.put(label,530,0)
		self.entry=gtk.Entry()
		self.entry.set_size_request(150,25)
		fixed.put(self.entry,530,17)
		button=gtk.Button('高级选项')
		button.set_size_request(100,25)
		fixed.put(button,100,55)
		button=gtk.Button('一键配置')
		button.set_size_request(100,25)
		button.connect('clicked',self.write_ha_config,[self.combox1,self.combox2,self.entry])
		fixed.put(button,580,55)
	def set_custom_model(self,widget):
		liststore=gtk.ListStore(str)
		if os.path.isfile('db/server.db'):
			conn=sqlite3.connect('db/server.db')
			cursor=conn.cursor()
			cursor.execute("select hostname from server where role='%s'" % self.index)
			while True:
				data=cursor.fetchone()
				if data is None:
					break
				host=str(data[0])
				liststore.append([host])
			cursor.close()
			conn.close()
		widget.set_model(liststore)	
		return 
	def write_jdbc_config(self,widget,entry):
		jdbc=entry.get_text()
		T=SaveJdbcConfig(jdbc)
		T.setDaemon(True)
		T.start()
	def write_ha_config(self,widget,data):
		master=data[0].get_active_text()
		slave=data[1].get_active_text()
		vip=data[2].get_text()
		T=SaveHAConfig(master,slave,vip)
		T.setDaemon(True)
		T.start()
	def _expose(self,widget,event):
		self.set_custom_model(self.combox1)
		self.set_custom_model(self.combox2)
	def insert_text(self,entry,text,length,position,data):
                #print 'hhhh'
                data[0].set_sensitive(True)
                data[1].set_sensitive(True)
        def delete_text(self,entry,start,end,data):
                if start == 0:
                        data[0].set_sensitive(False)
                        data[1].set_sensitive(False)
                
	
