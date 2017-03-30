"""Author: Jianming Zeng"""

class surfaceMap:
	
	## Local Variables

	hashMap = dict() ## key: identity 
	keySet = set()  ## store identity 
	surfaceCounter = 0

	
	"""
	Insert a list of surface objects into local hashMap 
	Argument: 
		aList: list of surface objects
			a surface object has surfaceNumber, nodeA, nodeB, nodeC, nodeD
				nodes are ordered in counterclockwise
	"""
	# def insert(self, aList):
	# 	for surface in aList:
	# 		identity = surface.getIdentity()
	# 		self.surfaceCounter += 1
	# 		if identity in self.keySet: 
	# 			self.hashMap[identity].append(surface)
	# 			print self.surfaceCounter, self.hashMap[identity]
	# 		else:
	# 			self.hashMap[identity] = [surface]
	# 			self.keySet.add(identity)
	# 			print self.surfaceCounter, self.hashMap[identity]

	def insert(self, aList):
		for surface in aList:
			surfaceNum, a, b, c, d, id = surface
			a, b, c, d = sorted([a, b, c, d])
			if (a,b,c,d) in self.keySet:
				self.hashMap[(a,b,c,d)].append(surface)
			else:
				self.hashMap[(a,b,c,d)] = [surface]
				self.keySet.add((a,b,c,d))

	def getHashMap(self, ):
		return self.hashMap