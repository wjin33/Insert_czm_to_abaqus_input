"""Author: Jianming Zeng"""

from node import *
from surface import *

class Element:
	
	## Local variables
	id = None
	node1 = None
	node2 = None
	node3 = None
	node4 = None
	node5 = None
	node6 = None
	node7 = None
	node8 = None
	nodeList = None

	surface1 = None
	surface2 = None
	surface3 = None
	surface4 = None
	surface5 = None
	surface6 = None

	order = None

	def __init__(self, id, a, b, c, d, e, f, g, h):
		## except for id, arguments are all node object
		self.id = id
		self.node1 = a
		self.node2 = b
		self.node3 = c
		self.node4 = d
		self.node5 = e
		self.node6 = f
		self.node7 = g
		self.node8 = h
		self.nodeList = [a, b, c, d, e, f, g, h]
		self.order = [a.getId(), b.getId(), c.getId(), d.getId(), e.getId(), f.getId(), 
			g.getId(), h.getId()]
		self.constructSurfaces()

	"""
	Contructing all six surfaces. For surfaces detail information please check abaqus manual for
	cohesive zone element
	"""  
	def constructSurfaces(self,):
		# self.surface1 = surface(1, self.node1.getId(), self.node2.getId(), 
		# 	self.node3.getId(), self.node4.getId(), self.id)
		# self.surface2 = surface(2, self.node5.getId(), self.node8.getId(), 
		# 	self.node7.getId(), self.node6.getId(), self.id)
		# self.surface3 = surface(3, self.node1.getId(), self.node5.getId(), 
		# 	self.node6.getId(), self.node2.getId(), self.id)
		# self.surface4 = surface(4, self.node2.getId(), self.node6.getId(), 
		# 	self.node7.getId(), self.node3.getId(), self.id)
		# self.surface5 = surface(5, self.node3.getId(), self.node7.getId(), 
		# 	self.node8.getId(), self.node4.getId(), self.id)
		# self.surface6 = surface(6, self.node4.getId(), self.node8.getId(), 
		# 	self.node5.getId(), self.node1.getId(), self.id)
		self.surface1 = (1, self.node1.getId(), self.node2.getId(), 
			self.node3.getId(), self.node4.getId(), self.id)
		self.surface2 = (2, self.node5.getId(), self.node8.getId(), 
			self.node7.getId(), self.node6.getId(), self.id)
		self.surface3 = (3, self.node1.getId(), self.node5.getId(), 
			self.node6.getId(), self.node2.getId(), self.id)
		self.surface4 = (4, self.node2.getId(), self.node6.getId(), 
			self.node7.getId(), self.node3.getId(), self.id)
		self.surface5 = (5, self.node3.getId(), self.node7.getId(), 
			self.node8.getId(), self.node4.getId(), self.id)
		self.surface6 = (6, self.node4.getId(), self.node8.getId(), 
			self.node5.getId(), self.node1.getId(), self.id)

	"""
	Helper function to get all the surface objects associated with the current element
	return: 
		a tuple of surface objects
	"""
	def getSurfaces(self):
		return self.surface1, self.surface2, self.surface3, 
		self.surface4, self.surface5, self.surface6 


	def updateNode(self, id, newNode):
		index = self.order.index(id)
		self.order[index] = newNode.getId()
		self.nodeList[index] = newNode


	def getId(self):
		return self.id

	def getString(self):
		return ', '.join(str(x) for x in self.order) + " \n"