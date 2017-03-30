"""Author: Jianming Zeng"""
from node import *

class surface:

	## Local variables
	surfaceNumber = None
	nodeA = None
	nodeB = None
	nodeC = None
	nodeD = None
	elementID = None


	def __init__(self, num, a, b, c, d, id):
		self.surfaceNumber = num
		self.nodeA = a 
		self.nodeB = b
		self.nodeC = c
		self.nodeD = d
		self.elementID = id


	"""
	Identity is NOT the surface number of the surface. This Identity is a tuple of nodes' 
	ID which is used for comparison between surface objects. It's sorted in an accending 
	order. 

	return:
		a tuple of ndoes' ID in accending order 
	"""
	def getIdentity(self):
		a, b, c, d = sorted([self.nodeA.getId(), self.nodeB.getId(), self.nodeC.getId(), self.nodeD.getId()])
		return (a, b, c, d)

	def getNodes(self, ):
		return (self.nodeA, self.nodeB, self.nodeC, self.nodeD)

	def getSurfaceNum(self, ):
		return self.surfaceNumber

	def getElementID(self,):
		return self.elementID