# -*- coding: utf-8 -*-
import subprocess
import os
import config
CORE = config.core_manager_source_path
def branch(path):
	branch = ''
	proc = subprocess.Popen(['git', '-C', path, 'branch'], stdout=subprocess.PIPE)
	while True:
		line = proc.stdout.readline()
		if len(line) and line[0] == '*':
			branch = line.split(' ')[1].strip()
			break
	return branch.replace('/', '-')

def ssh(host, command):
	print 'ssh -A root@%s "%s"' % (host, command)
	subprocess.call('ssh -A root@%s "%s"' % (host, command), shell=True)
def sshout(host, command):
	print 'ssh -A root@%s "%s"' % (host, command)
	try:
		return subprocess.check_output('ssh -A root@%s "%s"' % (host, command), shell=True)
	except subprocess.CalledProcessError:
		return ''
def cp(host, src, dst):
	print src, dst
	subprocess.call('rsync -cvr --exclude .build --exclude .git %s root@%s:%s' % (src, host, dst), shell=True)
	#subprocess.call('rsync -ctvr --delete --exclude .build --exclude .git %s root@%s:%s' % (src, host, dst), shell=True)
def initdistdir(server):
	dirname = os.path.basename(os.path.normpath(os.getcwd()))
	if dirname == 'core-manager':
		return
	#Возможно нужно удалять дист постоянно
	dst = destination(CORE)
	cp(server, CORE + '/', dst)
	ssh(server, 'cd {} && gmake -j5 dist DISTDIR={}'.format(dst, get_base()))
def get_base():
	#Возможно стоит использовать и папку панели с бранчем
	dirname = os.path.basename(os.path.normpath(os.getcwd()))
	if dirname == 'core-manager':
		return ''
	return destination(CORE) + "-dist"
def destination(path=os.getcwd()):
	dirname = os.path.basename(os.path.normpath(path))
	return os.path.join("/root", dirname + "-" + branch(path))
