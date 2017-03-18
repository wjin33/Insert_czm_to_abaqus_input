"""Author: Jianming Zeng"""

class surfaceMap:
	
	## Local Variables

	hashMap = None
	keySet = None
	surfaceCounter = 0

	def __init__(self, ):
		hashMap = dict() ## key: identity 
		keySet = set()  ## store identity 


	"""
	Insert a list of surface objects into local hashMap 
	Argument: 
		aList: list of surface objects
			a surface object has surfaceNumber, nodeA, nodeB, nodeC, nodeD
				nodes are ordered in counterclockwise
	"""
	def insert(self, aList):
		for surface in aList:
			identity = surface.getIdentity()
			if identity in keySet: 
				hashMap[identity].append(surface)
			else:
				hashMap[identity] = [surface]
				keySet.add(identity)
