# -*- coding: utf-8 -*-

import sys,os
import time
import socket
from ftplib import FTP

sys.path.append('G:\\code\\Tools\\configfile')
from configure_all import *

class ftp_file(object):
	"""
	connect to ftp server, get or put file.
	"""
	def __init__(self):
		pass

	def con_server(self, serverip, serverport='21', user='anonymous', passwd='anonymous'):
		self.serverip = serverip
		ftp = FTP()
		ftp.set_debuglevel(2)
		ftp.connect(serverip, int(serverport))
		ftp.login(user, passwd)
		return ftp

	def get_file(self, ftp, path, filename):
		buffsize = 1024
		self.ftp = ftp
		self.filename = '%s-%s.avc' % (av_version, av_newversion)
		print(ftp.getwelcome())
		fp = open('%s%s' % (path, filename), 'wb')
		ftp.retrbinary('RETR %s' % (filename), fp.write, buffsize)
		# ftp.set_debuglevel(0)
		time.sleep(10)
		fp.close()

if __name__ == '__main__':
	ftp = ftp_file()
	filename = '%s-%s.avc' % (av_version, av_newversion)
	ftpsession = ftp.con_server(ftpserver, serverport, user, passwd)
	ftp.get_file(ftpsession, avfile_path, filename)