#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import remote
import sys
import config
DEFAULT_HOST = config.build_server

def upload_source(args):
	server = args[1]
	dst = remote.destination()
	remote.ssh(server, 'mkdir -p {}'.format(dst))
	remote.cp(server, os.getcwd() + '/', dst)
def remove_source(args):
	server = args[1]
	dst = remote.destination()
	remote.ssh(server, 'rm -rf {}'.format(dst))
def main():
	args = sys.argv[1:]
	server = DEFAULT_HOST
	if len(args) >= 2:
		if args[0] == 'source':
			upload_source(args)
			return
		if args[0] == 'nosource':
			remove_source(args)
			return
	remote.initdistdir(server)
	base = remote.get_base()
	dst = remote.destination()
	remote.ssh(server, 'mkdir -p {}'.format(dst))
	remote.cp(server, os.getcwd() + '/', dst)
	remote.ssh(server, 'cd {} && gmake {} {}'.format(dst, 'BASE=' + base if len(base) else '', ' '.join(args)))

if __name__ == '__main__':
	main()
