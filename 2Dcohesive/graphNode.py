class graphNode:
	ID = None
	neighbours = None
	number = 0

	def __init__(self, ID):
		self.ID = int(ID)
		self.neighbours = []
		self.number = 0

	def addNeighbour(self, node):
		self.neighbours += [node]
		self.number += 1


