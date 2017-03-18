## Author: Jianming Zeng

class node:
	
	## Local variables
	id = None
	x = None
	y = None
	z = None


	def __init__(self, id, x, y, z):
		self.id = id
		self.x = x
		self.y = y
		self.z = z
	
	
	def getId(self):
		return self.id