class Coords:
	def __init__(self, inputType='index', data, width=None):
		if(inputType == 'tuple'):
			self.coordTup = data

		elif (inputType == 'index'):
			self.index = data
			self.coordTup = indexToCoords(self.index, width, 'tuple')

		self.x = data[0]
		self.y = data[1]

	def __str__(self):
		return '('+self.x+','+self.y+')'

	def getCoords

def indexToCoords(index, width,returnType='obj'):
	y = index / width
	x = (index - 1) % width

	if(returnType == 'obj'):
		return Coords(inputType='tuple', data=(x,y))
	else:
		return (x,y)

