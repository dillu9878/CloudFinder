'''
	Counts how many pixels that satisfy the condition given, with a center of the startpx.

'''
pixelsFound = 0
cleanedAreas = []
class sideDataAssoc:
	def __init__(self, data):
		self.top = data[0]
		self.right = data[1]
		self.bottom = data[2]
		self.left = data[3]

class simpleImage:
	def __init__(self, PILimage):
		self.height = PILimage.size[1]
		self.width = PILimage.size[0]
		self.pixels = list(PILimage.getdata())

class pixel:
	def __init__(self, img, ref, condition,lastPx):
		self.surrounds = checkSides(img, ref, condition)
		self.previousPx = lastPx
		self.nextPx = 0
	def move():
		

# returns a tuple with data about the four sides of the image of format (top, right, bottom, left)
def checkSides(im, startpx, condition, returnType='tuple'):
	global pixelsFound
	global cleanedAreas

	sideData = ()

	pxRefs = (startpx + im.width, startpx + 1, startpx - im.width, startpx - 1)

	for pxref in pxRefs:
		if(pxref not in cleanedAreas):
			cleanedAreas.append(pxref)
			if(condition(im.pixels[pxref])):
				sideData = sideData + tuple([True])
				pixelsFound = pixelsFound + 1
			else:
				sideData = sideData + tuple([False])

	if(returnType != 'tuple'):
		return sideDataAssoc(sideData)
	else:
		return sideData

def findClumps(image, startpx, condition):
	global pixelsFound
	global cleanedAreas

	cleanedAreas.append(startpx)
	pixelsFound = 1
	im = simpleImage(image)
	while 
	for whitePx in checkSides(image, startpx, condition):
