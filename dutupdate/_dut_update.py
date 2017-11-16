#-*- coding=UTF-8 -*-

import telnetlib,encodings,sys

def _unicode_to_utf(unistr):
	return unicode(unistr).encode(encoding='UTF-8',errors='strict')

class _dut_update():

	def do_telnet_dut(self,host,port,username,password,commands=None,searchchar=None,expectation=None):
		'''
		telnet the dut,check the version&platform
		'''
		
		host=_unicode_to_utf(host)
		port=_unicode_to_utf(port)
		username=_unicode_to_utf(username)
		password=_unicode_to_utf(password)
		commands=_unicode_to_utf(commands)
		searchchar=_unicode_to_utf(searchchar)
		expectation=_unicode_to_utf(expectation)
		
		tn = telnetlib.Telnet(host,port)
		tn.set_debuglevel(2)
		
		tn.read_until('Username: ')
		tn.write(username + '\n')
		
		if(password != ''):
			tn.read_until('Password: ')
			tn.write(password + '\n')
			
		tn.read_until('host> ')
		tn.write(commands + '\n')
		
		
	
	def do_check_image():
		pass
	
	def do_update_image():
		pass
	
	def do_reboot_dut():
		pass
	
	def do_check_version():
		pass

if __name__ == "__main__":

	print "do debug"
	ts = _dut_update()
	ts.do_telnet_dut('172.17.10.131','23','admin','admin','enable')