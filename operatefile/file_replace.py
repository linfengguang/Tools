# -*- coding: utf-8 -*-

import sys
import time

class file_replace(object):
	"""replace the string in file"""
	def __init__(self):
		pass;

	def _text_replace(self, filename, sig, newstr):
		replace_data = ''
		with open(filename, 'r', encoding='utf-8') as file:
			for line in file:
				if sig in line:
					line = line.replace(sig, newstr)
				replace_data += line
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(replace_data)

	def _sig_locat(self, filename, keyword, offset):
	    sig_str = ''
	    with open(filename, 'r', encoding='utf-8') as file:
	    	for line in file:
	    		if keyword in line:
	    			sig_str = line[line.index(keyword)+len(keyword):line.index(keyword)+len(keyword)+offset]
	    return(sig_str)	

if __name__ == '__main__':

	test = file_replace()
	oldstr = test._sig_locat('config_lin.py', "av_version='", 8)
	oldstr2 = test._sig_locat('config_lin.py', "av_newversion='", 8)
	newstr = str(time.strftime('%Y%m%d', time.localtime()))
	if oldstr2 >= newstr :
		print('the old str eq to new str, nothing to do!')
		sys.exit(0)
	else:
		test._text_replace('config_lin.py', oldstr2, newstr)
		print('replace %s to %s' % (oldstr2, newstr))
	test._text_replace('config_lin.py', oldstr, oldstr2)