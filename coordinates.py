class Coords:
	def __init__(self, data, width=None, inputType='index'):
		if(inputType == 'tuple'):
			self.coordTup = data
		elif(inputType == 'index'):
			self.index = data
			self.coordTup = indexToCoords(self.index, width, 'tuple')
		else:
			print 'Well, something seems to be quite wrong with your inputType argument...'
		
		self.x = self.coordTup[0]
		self.y = self.coordTup[1]

	def __str__(self):
		return '('+self.x+','+self.y+')'

	def getCoords(self):
		return self.coordTup

def indexToCoords(index, width,returnType='obj'):
	y = index / width
	x = (index-1) % width

	coordTup = (x,y)

	if(returnType == 'obj'):
		return Coords(coordTup, inputType='tuple')
	else:
		return coordTup

if(__name__ == '__main__'):
	print Coords(6,3).getCoords()