from socket import *
import pinfo, common, maze, sys, os

try:
	HOST = ''
	PORT = 9876
	s = socket(AF_INET6,SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(5)
	while True:
		conn,addr = s.accept()
		print 'Connected by',addr
		if os.fork() == 0:
			#Child
			cli = pinfo.pinfo(conn,addr)
			prompt = '> '
			while True:
				if cli.exploring:
					cli.process('show')
				conn.sendall(prompt)
				line = conn.recv(1024)[:-2]
				if line == 'quit':
					break
				if line == '':
					continue
				cli.process(line)
			conn.close()
		else:
			conn.close()
except KeyboardInterrupt:
	pass
