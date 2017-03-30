"""Author: Jianming Zeng"""

from node import *
from Element import *
from surface import *
from surfaceMap import *

class graph: 

	## Local variables and data strcuctures
	name = None

	nodeMap = dict()
	nodes = 0
	elementMap = dict()
	elements = 0
	mySurfaceMap = None

	surfList = list()
	surfaceCount = 1
	CPList = list()
	cohList = list()

	## Tracker update 
	nodeTracker = dict()

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

		newElement = Element(id, a, b, c, d, e, f, g, h)
		self.elementMap[id] = newElement
		self.elements += 1
		self.insertSurfaces(newElement)
		# print "current Element ID " + str(id)
		# print newElement.nodes.keys()

	"""
	This function pairs every surface which is shared by two elements.
	The idea is that if any two elements have the exact same nodes' id 
	in the surfaces, then those two surfaces are actually shared. We 
	record it for later use
	Argument:
		element: new element object 
	"""
	def insertSurfaces(self, myElement):
		surfaces = myElement.getSurfaces()
		self.mySurfaceMap.insert(surfaces)



	def getElementByID(self, id):
		return self.elementMap[id]


	def getSurfaceMap(self, ):
		return self.mySurfaceMap

	def homogeneous(self, start, stop, step):
		hashMap = self.mySurfaceMap.getHashMap()
		tacker = set()
		for key in hashMap:
			if len(hashMap[key]) == 2:
				myList = [] 
				surface1, surface2 = hashMap[key]
		
				element1 = self.getElementByID(surface1[5])
				surfaceNumber1 = surface1[0]
				nodes1 = (self.getNodeByID(surface1[1]),
						self.getNodeByID(surface1[2]),
						self.getNodeByID(surface1[3]),
						self.getNodeByID(surface1[4]),
					)
				
				element2 = self.getElementByID(surface2[5])
				surfaceNumber2 = surface2[0]
				nodes2 = (self.getNodeByID(surface2[1]),
						self.getNodeByID(surface2[2]),
						self.getNodeByID(surface2[3]),
						self.getNodeByID(surface2[4]),
					)

				## update node directly 
				myList += self.updateNode(nodes1, element1)
				myList += self.updateNode(nodes2, element2)

				self.cohList.append(myList)
				self.surfList.append(["surface"+str(self.surfaceCount), 
						str(element1.getId()), "S" + str(surfaceNumber1)])
				self.surfList.append(["surface"+str(self.surfaceCount+1), 
						str(element2.getId()), "S" + str(surfaceNumber2)])
				self.CPList.append (("surface"+str(self.surfaceCount), "surface"+str(self.surfaceCount+1)))
				self.surfaceCount+=2
                


	def updateNode(self, nodes, element):
		myList = []
		for current in nodes:
			if current.getId() in self.nodeTracker:	
				self.nodes += 1
				id = current.getId()
				current = node(self.nodes, current.x, current.y, current.z)
				self.nodeMap[self.nodes] = current
				element.updateNode(id, current)
			else:
				self.nodeTracker[current.getId()] = []


			myList.append(current.getId())
		return myList

