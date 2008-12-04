import common, maze, character
from maze import ENTRANCE, COFFERS, WEST, SOUTH, EAST, NORTH

class pinfo:
	def __init__(self,conn,addr,ctr=None,maz=None):
		self.ctr = ctr
		self.maz = maz
		self.conn = conn
		self.addr = addr
		self.exploring = False
		self.helpstr = 'Commands currently available:\nload\tshow\thelp\n'
	def loadMaze(self,mname):
		self.maz = maze.maze(maze.mfname(mname))
	def process(self,line):
		args = line.split()
		if args[0] == 'load':
			try:
				self.loadMaze(args[1])
			except:
				self.maz = None
		elif args[0] == 'show':
			if self.maz == None:
				return
			chars = []
			for i in range(2*self.maz.width+1):
				chars.append([])
				for j in range(2*self.maz.height+1):
						chars[i].append(' ')
			if self.exploring:
				xmin = max(0,self.ctr.x-5)
				xmax = min(self.maz.width,self.ctr.x+6)
				ymin = max(0,self.ctr.y-5)
				ymax = min(self.maz.height,self.ctr.y+6)
			else:
				xmin = 0
				xmax = self.maz.width
				ymin = 0
				ymax = self.maz.height
			for i in range(xmin,xmax):
				for j in range(ymin,ymax):
					if not self.exploring or self.visible[i][j]:
						chars[2*i][2*j]='@'
						chars[2*i+2][2*j]='@'
						chars[2*i][2*j+2]='@'
						chars[2*i+2][2*j+2]='@'
						c = self.maz.cell(i,j)
						if c & ENTRANCE:
							chars[2*i+1][2*j+1]='I'
						if c & COFFERS:
							chars[2*i+1][2*j+1]='C'
						if self.exploring:
							if i == self.ctr.x and j == self.ctr.y:
								chars[2*i+1][2*j+1]='*'
						if c & WEST:
							chars[2*i][2*j+1]='@'
						if c & SOUTH:
							chars[2*i+1][2*j+2]='@'
						if c & EAST:
							chars[2*i+2][2*j+1]='@'
						if c & NORTH:
							chars[2*i+1][2*j]='@'
			outstr = ''
			for y in range(2*self.maz.height+1):
				for x in range(2*self.maz.width+1):
					outstr += chars[x][y]
				outstr+='\n'
			self.conn.sendall(outstr)
			if self.exploring:
				descr = ''
				if self.ctr.x == self.maz.ix and self.ctr.y == self.maz.iy:
					descr += 'There is an exit here.\n'
				if self.ctr.x == self.maz.cx and self.ctr.y == self.maz.cy:
					descr += 'The coffers are located here\n'
				self.conn.sendall(descr)
		elif args[0] == 'help':
			self.conn.sendall(self.helpstr)
		elif args[0] == 'explore':
			if self.maz==None:
				return
			self.exploring = True
			if self.ctr == None:
				self.ctr = character.character()
			self.ctr.x = self.maz.ix
			self.ctr.y = self.maz.iy
			self.visible=[]
			for i in range(self.maz.width):
				self.visible.append([])
				for j in range(self.maz.height):
					self.visible[i].append(False)
			self.visible[self.maz.ix][self.maz.iy]=True
		elif args[0] == 'n':
			if not self.exploring:
				return
			if self.maz.cell(self.ctr.x,self.ctr.y) & NORTH:
				return
			self.ctr.y-=1
			self.visible[self.ctr.x][self.ctr.y]=True
		elif args[0] == 'e':
			if not self.exploring:
				return
			if self.maz.cell(self.ctr.x,self.ctr.y) & EAST:
				return
			self.ctr.x+=1
			self.visible[self.ctr.x][self.ctr.y]=True
		elif args[0] == 's':
			if not self.exploring:
				return
			if self.maz.cell(self.ctr.x,self.ctr.y) & SOUTH:
				return
			self.ctr.y+=1
			self.visible[self.ctr.x][self.ctr.y]=True
		elif args[0] == 'w':
			if not self.exploring:
				return
			if self.maz.cell(self.ctr.x,self.ctr.y) & WEST:
				return
			self.ctr.x-=1
			self.visible[self.ctr.x][self.ctr.y]=True
		elif args[0] == 'n':
			if not self.exploring:
				return
			if self.maz.cell(self.ctr.x,self.ctr.y) & NORTH:
				return
			self.ctr.y-=1
			self.visible[self.ctr.x][self.ctr.y]=True
		else:
			self.conn.sendall('What?\n')
