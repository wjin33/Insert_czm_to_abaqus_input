"""Author: Jianming Zeng"""
from node import *

class surface:

	## Local variables
	surfaceNumber = None
	nodeA = None
	nodeB = None
	nodeC = None
	nodeD = None


	def __init__(self, num, a, b, c, d):
		self.surfaceNumber = num
		self.nodeA = a 
		self.nodeB = b
		self.nodeC = c
		self.nodeD = d

	"""
	Identity is NOT the surface number of the surface. This Identity is a tuple of nodes' 
	ID which is used for comparison between surface objects. It's sorted in an accending 
	order. 

	return:
		a tuple of ndoes' ID in accending order 
	"""
	def getIdentity(self):
		return [nodeA.getId(), nodeB.getId(), nodeC.getId(), nodeD.getId()].sort()