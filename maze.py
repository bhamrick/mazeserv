import common

ENTRANCE = 0x10
COFFERS = 0x20
WEST = 0x08
SOUTH = 0x04
EAST = 0x02
NORTH = 0x01

def mfname(mname):
	return common.BASEPATH + '/mazes/' + mname + '.maz'

class maze:
	def __init__(self,filename):
		fin = open(filename,"r")
		dims = fin.readline().split()
		self.width = int(dims[0])
		self.height = int(dims[1])
		instr = fin.read()
		self.data = []
		for i in range(self.width):
			self.data.append([])
			for j in range(self.height):
				self.data[i].append(ord(instr[j*self.width+i]))
				print self.data[i][j]
				if ord(instr[j*self.width+i]) & 0x20 != 0:
					self.cx = i
					self.cy = j
				if ord(instr[j*self.width+i]) & 0x10 != 0:
					self.ix = i
					self.iy = j
	def cell(self,x,y):
		return self.data[x][y]
