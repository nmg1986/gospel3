#!/usr/bin/python


import paramiko
import socket
import errno

AUTHFAILED=1
UNREACH=2
TIMEOUT=3
REFUSED=4
HOSTUNREACH=5

class SSHClient():
	def __init__(self):
		self.ssh=paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	def connect(self,username,password,hostname,port):
		try:
			self.ssh.connect(hostname=hostname,port=port,username=username,password=password,timeout=60)
			return 0
		except paramiko.AuthenticationException:
			return AUTHFAILED 
		except socket.error as e:
			if e.errno == errno.ENETUNREACH:
				return UNREACH 
			if e.errno == errno.ETIMEDOUT:
				return TIMEOUT 
			if e.errno == errno.ECONNREFUSED:
				return REFUSED 
	def upload(self,localfile,remotefile):
		self.sftp=self.ssh.open_sftp()
		self.sftp.put(localfile,remotefile)
	def execute(self,command):
		self.channel=self.ssh.get_transport().open_session()
		self.channel.exec_command(command)
		return self.channel.recv_exit_status()
	def close(self):
		self.sftp.close()
		self.ssh.close()
