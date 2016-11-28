class treeNode:
	ID = None
	parent = None
	child = None
	num = 0

	def __init__(self, ID):
		self.ID = int(ID)
		self.child = []
		self.parent = []

	def addParent(self, parent):
		self.parent += [parent]
		self.num += 1

	def addChild(self, child):
		self.child += [child]
		self.num += 1
