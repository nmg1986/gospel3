#!/usr/bin/python
#-*- coding:utf-8 -*-


import gtk
import heartbeat
import sqlite3
import os
import paramiko
import threading
import time

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
		ssh.exec_command("echo nginx-master IPaddr::%s nginx memcached solomon > /etc/ha.d/haresources" % self.vip)
		progressLabel.set_text('正在配置进程监控...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("/usr/bin/sed -i '/^#\[nginx\]/,+2 s/^#//'     /etc/solomon.conf")
		ssh.exec_command("/usr/bin/sed -i '/^#\[memcached\]/,+2 s/^#//' /etc/solomon.conf")
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
		ssh.exec_command("echo nginx-master IPaddr::%s nginx memcached solomon > /etc/ha.d/haresources" % self.vip)
		progressLabel.set_text('正在配置进程监控...')
		progressBar.set_fraction(0.7)
		progressBar.set_text('70%')
		ssh.exec_command("sed -i '/^#\[nginx\]/,+2 s/^#//'     /etc/solomon.conf")
		ssh.exec_command("sed -i '/^#\[memcached\]/,+2 s/^#//' /etc/solomon.conf")
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

class SaveNginxConfig(threading.Thread):
	def __init__(self):
		self.weblist=[]
		self.clientlist=[]
		self.waplist=[]
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
		progressLabel.set_text('正在获取中间件服务器列表...')
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute("select hostname from server where role='1'")
		data=cursor.fetchall()
		if data is not None:
			for host in data:
				self.clientlist.append(str(host[0]))	
			print self.clientlist
		cursor.close()
		progressBar.set_fraction(0.2)
		progressBar.set_text('20%')
		progressLabel.set_text('正在获取管理平台服务器列表...')
		cursor.execute("select hostname from server where role='2'")
		data=cursor.fetchall()
		if data is not None:
			for host in data:
				self.weblist.append(str(host[0]))
		print self.weblist
		cursor.close()
		progressBar.set_fraction(0.3)
		progressBar.set_text('30%')
		progressLabel.set_text('正在配置nginx...')
		cursor.execute("select hostname from server where role='0'")
		data=cursor.fetchall()
		if data is not None:
			for host in data:
				hostname=str(host[0])

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
				ssh.exec_command('mv /usr/nginx/conf/{nginx.conf,nginx.conf.bak}')
				ssh.exec_command('cat /dev/null > /usr/nginx/conf/nginx.conf')
				ssh.exec_command('''
						echo "user  nobody nobody;" >> /etc/nginx.conf
						echo "worker_processes  8;" >> /etc/nginx.conf
						echo "worker_rlimit_nofile 65535;" >> /etc/nginx.conf
						echo "error_log  /var/log/nginx/error.log notice;" >> /etc/nginx.conf
						echo "pid        /var/run/nginx.pid;" >> /etc/nginx.conf
						echo                                  >> /etc/nginx.conf	
							
						echo "events {                      " >> /etc/nginx.conf
						echo -e "\tuse epoll;               " >> /etc/nginx.conf 
						echo -e "\tworker_connections      65535;" >> /etc/nginx.conf
						echo "}"                                   >> /etc/nginx.conf

						echo "http {                        " >> /etc/nginx.conf
						echo -e "\tinclude       mime.types;" >> /etc/nginx.conf
						echo -e "\tdefault_type  application/octet-stream;" >> /etc/nginx.conf
						echo -e "\tlog_format main  '\$time_local||| \$http_x_forwarded_for ||| \$cookie_jsessionid ||| \$remote_addr ||| \$uri ||| \$request_uri ||| \$upstream_addr';" >> /etc/nginx.conf
	    				echo >> /etc/nginx.conf 
						echo -e "\tgzip on;" >> /etc/nginx.conf
						echo -e "\tgzip_min_length  1k;" >> /etc/nginx.conf
						echo -e "\tgzip_buffers     4 16k;" >> /etc/nginx.conf
						echo -e "\tgzip_http_version 1.1;" >> /etc/nginx.conf
						echo -e "\tgzip_types    text/plain application/x-javascript text/css  application/xml;" >> /etc/nginx.conf
	
						echo -e "\taccess_log  /var/log/nginx/access.log main;" >> /etc/nginx.conf
	
						echo -e "\tclient_header_timeout  1m;" >> /etc/nginx.conf
						echo -e "\tclient_body_timeout    1m;" >> /etc/nginx.conf
						echo -e "\tsend_timeout           1m;"  >> /etc/nginx.conf
						echo -e "\tsendfile                on;" >> /etc/nginx.conf
	
						echo -e "\ttcp_nopush              on;" >> /etc/nginx.conf
						echo -e "\ttcp_nodelay             on;" >> /etc/nginx.conf
	
						echo -e "\tkeepalive_timeout  300;" >> /etc/nginx.conf

						echo -e "\tupstream tomcat_web {" >> /etc/nginx.conf
						list=$(echo %s | sed 's/\[//' | sed 's/\]//' | tr ',' ' ')
						for host in $list 
						do 
							echo -e "\t\tserver ${host}:8080  srun_id=$(echo $host | sed 's/\.//g');" >> /etc/nginx.conf
						done
                		echo -e "\t\tjvm_route $cookie_JSESSIONID reverse;" >> /etc/nginx.conf
						echo -e "\t\tcheck interval=3000 rise=2 fall=5 timeout=1000;" >> /etc/nginx.conf
						echo -e "\t}" >> /etc/nginx.conf
						echo -e "\tupstream tomcat_client {" >> /etc/nginx.conf
						list=$(echo %s | sed 's/\[//' | sed 's/\]//' | tr ',' ' ')
						for host in $list 
						do 
							echo -e "\t\tserver ${host}:8080  srun_id=$(echo $host | sed 's/\.//g');" >> /etc/nginx.conf
						done
                		echo -e "\t\tjvm_route $cookie_JSESSIONID reverse;" >> /etc/nginx.conf
						echo -e "\t\tcheck interval=3000 rise=2 fall=5 timeout=1000;" >> /etc/nginx.conf
						echo -e "\t}" >> /etc/nginx.conf
						echo -e "\tupstream tomcat_wap {" >> /etc/nginx.conf
						list=$(echo %s | sed 's/\[//' | sed 's/\]//' | tr ',' ' ')
						for host in $list 
						do 
							echo -e "\t\tserver ${host}:8080  srun_id=$(echo $host | sed 's/\.//g');" >> /etc/nginx.conf
						done
                		echo -e "\t\tjvm_route $cookie_JSESSIONID reverse;" >> /etc/nginx.conf
						echo -e "\t\tcheck interval=3000 rise=2 fall=5 timeout=1000;" >> /etc/nginx.conf
						echo -e "\t}" >> /etc/nginx.conf
    	
						echo -e "\tserver {"           >> /etc/nginx.conf
						echo -e "\t\tlisten         80;" >> /etc/nginx.conf
						echo -e "\t\tserver_name    localhost;" >> /etc/nginx.conf
						echo -e "\t\tcharset utf-8;" >> /etc/nginx.conf
      					echo -e "\t\tlocation / {" >> /etc/nginx.conf
		        		echo -e "\t\t\tproxy_pass      http://tomcat_web;" >> /etc/nginx.conf
                  		echo -e "\t\t\tproxy_redirect          off;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        Host $host;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Real-IP $remote_addr;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;" >> /etc/nginx.conf
                  		echo -e "\t\t\tproxy_next_upstream error timeout invalid_header http_500 http_503;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffering off;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_max_body_size    50m;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_body_buffer_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_connect_timeout   300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_send_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_read_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffer_size        4k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffers           8 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_busy_buffers_size   128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_temp_file_write_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t}" >> /etc/nginx.conf	

						echo -e "\t\tlocation  /http.do {" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_pass      http://tomcat;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_redirect          off;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        Host $host;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Real-IP $remote_addr;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_next_upstream error timeout invalid_header http_500 http_503;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffering off;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_max_body_size    50m;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_body_buffer_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_connect_timeout   300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_send_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_read_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffer_size        4k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffers           8 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_busy_buffers_size   128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_temp_file_write_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t}" >> /etc/nginx.conf

						echo -e "\t\tlocation  /wap/m.do {" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_pass      http://tomcat;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_redirect          off;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        Host $host;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Real-IP $remote_addr;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_next_upstream error timeout invalid_header http_500 http_503;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffering off;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_max_body_size    50m;" >> /etc/nginx.conf
						echo -e "\t\t\tclient_body_buffer_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_connect_timeout   300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_send_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_read_timeout      300;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffer_size        4k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_buffers           8 128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_busy_buffers_size   128k;" >> /etc/nginx.conf
						echo -e "\t\t\tproxy_temp_file_write_size 128k;" >> /etc/nginx.conf
						echo -e "\t\t}" >> /etc/nginx.conf
		
						echo -e "\t\tlocation /NginxStatus {" >> /etc/nginx.conf
						echo -e "\t\t\tstub_status             on;" >> /etc/nginx.conf
						echo -e "\t\t\taccess_log              off;" >> /etc/nginx.conf
						echo -e "\t\t\tauth_basic              "NginxStatus";" >> /etc/nginx.conf
						echo -e "\t\t}" >> /etc/nginx.conf
						echo "\t}" >> /etc/nginx.conf
						echo "}" >> /etc/nginx.conf
		''' % (self.weblist,self.clientlist,self.clientlist)
		)
		progressBar.set_fraction(1.0)
		progressBar.set_text('100%')
		progressLabel.set_text('配置完毕')
		time.sleep(1)
		progressWin.destroy()
		
class InputConfig(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		self.set_border_width(20)
		self.connect('expose-event',self._expose)
		self.index=0
	
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
		entry=gtk.Entry()
		entry.set_size_request(150,25)
		fixed.put(entry,530,17)
		button=gtk.Button('高级选项')
		button.set_size_request(100,25)
		fixed.put(button,100,55)
		button=gtk.Button('一键配置')
		button.set_size_request(100,25)
		button.connect('clicked',self.write_ha_config,[self.combox1,self.combox2,entry])
		fixed.put(button,580,55)
		
		frame=gtk.Frame('nginx配置')
		frame.set_size_request(810,308)
		self.fixed.put(frame,0,150)
		fixed=gtk.Fixed()
		frame.add(fixed)
		frame1=gtk.Frame('集群配置')
		frame1.set_size_request(700,65)
		fixed.put(frame1,50,5)
		frame2=gtk.Frame('缓存配置')
		frame2.set_size_request(700,65)
		frame2.set_sensitive(False)
		fixed.put(frame2,50,75)
		frame3=gtk.Frame('正向代理配置')
		frame3.set_size_request(700,65)
		frame3.set_sensitive(False)
		fixed.put(frame3,50,145)
		frame4=gtk.Frame('https配置')
		frame4.set_size_request(700,65)
		frame4.set_sensitive(False)
		fixed.put(frame4,50,215)
		
		fixed=gtk.Fixed()
		frame1.add(fixed)
		#webbutton=gtk.CheckButton('web')
		#clientbutton=gtk.CheckButton('client')
		#wapbutton=gtk.CheckButton('wap')
		button1=gtk.Button('高级选项')
		button2=gtk.Button('一键配置')
		button1.set_size_request(100,25)
		button2.set_size_request(100,25)
		button2.connect('clicked',self.write_nginx_config)#,[webbutton,clientbutton,wapbutton])
		#fixed.put(webbutton,100,10)
		#fixed.put(clientbutton,350,10)
		#fixed.put(wapbutton,600,10)
		#fixed.put(button1,100,50)
		#fixed.put(button2,580,50)
		fixed.put(button1,100,10)
		fixed.put(button2,580,10)

		fixed=gtk.Fixed()
		frame2.add(fixed)
		#webbutton=gtk.CheckButton('web')
		#clientbutton=gtk.CheckButton('client')
		#wapbutton=gtk.CheckButton('wap')
		button1=gtk.Button('高级选项')
		button2=gtk.Button('一键配置')
		button1.set_size_request(100,25)
		button2.set_size_request(100,25)
		#fixed.put(webbutton,100,10)
		#fixed.put(clientbutton,350,10)
		#fixed.put(wapbutton,600,10)
		fixed.put(button1,100,10)
		fixed.put(button2,580,10)

		fixed=gtk.Fixed()
		frame3.add(fixed)
		label=gtk.Label('DNS')
		label.set_size_request(-1,-1)
		fixed.put(label,100,0)
		entry=gtk.Entry()
		entry.set_size_request(150,25)
		fixed.put(entry,100,20)
		button=gtk.Button('一键配置')
		button.set_size_request(100,25)
		fixed.put(button,580,20)

		fixed=gtk.Fixed()
		frame4.add(fixed)
		#webbutton=gtk.CheckButton('web')
		#clientbutton=gtk.CheckButton('client')
		#wapbutton=gtk.CheckButton('wap')
		button1=gtk.Button('高级选项')
		button2=gtk.Button('一键配置')
		button1.set_size_request(100,25)
		button2.set_size_request(100,25)
		#fixed.put(webbutton,100,10)
		#fixed.put(clientbutton,350,10)
		#fixed.put(wapbutton,600,10)
		fixed.put(button1,100,10)
		fixed.put(button2,580,10)
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
	def write_ha_config(self,widget,data):
		master=data[0].get_active_text()
		slave=data[1].get_active_text()
		vip=data[2].get_text()
		T=SaveHAConfig(master,slave,vip)
		T.setDaemon(True)
		T.start()
	def write_nginx_config(self,widget):
		T=SaveNginxConfig()
		T.setDaemon(True)
		T.start()
	def _expose(self,widget,event):
		self.set_custom_model(self.combox1)
		self.set_custom_model(self.combox2)
