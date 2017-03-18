## Author: Jianming Zeng
from node import *

class element:
	
	## Local variables
	id = None
	front1 = None
	front2 = None
	front3 = None
	front4 = None
	back1 = None
	back2 = None
	back3 = None
	back4 = None

	surface1 = None
	surface2 = None
	surface3 = None
	surface4 = None
	surface5 = None
	surface6 = None

	def __init__(self, id, a, b, c, d, e, f, g, h):
		## except for id, arguments are all node object
		self.id = id
		self.front1 = a
		self.front2 = b
		self.front3 = c
		self.front4 = d
		self.back1 = e
		self.back2 = f
		self.back3 = g
		self.back4 = h
		self.constructSurfaces()

	def constructSurfaces(self):
		pass


	def getSurfaces(self):
		return self.surface1, self.surface2, self.surface3, self.surface4, self.surface5, self.surface6 

	

