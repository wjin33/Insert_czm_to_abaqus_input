## Author: Jianming Zeng

from node import *
from element import *
from surface import *
from surfaceMap import *

class graph: 


	## Local variables and data strcuctures
	name = None

	nodeMap = dict()
	nodes = 0
	elementMap = dict()
	elements = 0
	surfaceMap = None
	

	"""
	Initialize an empty skeleton graph

	"""
	def __init__(self, name):
		self.name = name
		self.mySurfaceMap = surfaceMap()

	""" Node 
	Responsible for geting string information from the list
	Convert them accordingly and create new node 
	Argument: 
		infoList: A list of string in the format(id, x-axis, y-axis, z-axis)
	"""
	def addNode(self, infoList):
		id,x,y,z = infoList
		id = int(id.split(",")[0].strip())
		x = float(x.split(",")[0].strip())
		y = float(y.split(",")[0].strip())
		z = float(z.split(",")[0].strip())
		newNode = node(id, x, y, z)
		self.nodeMap[id] = newNode
		self.nodes += 1

	"""
	Helper functions, Do not access nodeMap directly
	Prevent data corruption
	Argument: 
		id: Id associated with the node(int)
	Return:
		node(object) 

	"""
	def getNodeByID(self, id):
		return self.nodeMap[id]


	"""
	Extract information from infoList
	then store these information into the element map, and construct 
	surfaces 
	Argument:
		infoList: a list of string in the form (id, frontNode1, frontNode2,
			frontNode3, frontNode4, backNode1, backNode2, backNode3, backNode4)
			nodes are ordered counterclowise, front four nodes come first, then
			back, and number indicates a neighbour relationship. Ex. frontNode1
			and backNode1 are connected
	"""
	def addElement(self, infoList):
		id, a, b, c, d, e, f, g, h = infoList 
		id = int(id.split(",")[0].strip())

		a = self.getNodeByID(int(a.split(",")[0].strip()))
		b = self.getNodeByID(int(b.split(",")[0].strip()))
		c = self.getNodeByID(int(c.split(",")[0].strip()))
		d = self.getNodeByID(int(d.split(",")[0].strip()))
		e = self.getNodeByID(int(e.split(",")[0].strip()))
		f = self.getNodeByID(int(f.split(",")[0].strip()))
		g = self.getNodeByID(int(g.split(",")[0].strip()))
		h = self.getNodeByID(int(h.split(",")[0].strip()))

		newElement = element(id, a, b, c, d, e, f, g, h)
		self.elementMap[id] = newElement
		self.elements += 1

		self.insertSurfaces(newElement)


	"""
	This function pairs every surface which is shared by two elements.
	The idea is that if any two elements have the exact same nodes' id 
	in the surfaces, then those two surfaces are actually shared. We 
	record it for later use
	Argument:
		element: new element object 
	"""
	def insertSurfaces(self, element):
		surfaces = element.getSurfaces()
		self.mySurfaceMap.insert(surfaces)


	def getElementByID(self, id):
		return self.elementMap[id]




