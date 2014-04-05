class SimpleImage:
	def __init__(self, PILimage):
		self.height = PILimage.size[1]
		self.width = PILimage.size[0]
		self.pixels = list(PILimage.getdata())

class LineSpaceFinder:
	def __init__(self, seed, condition, image):
		self.im = SimpleImage(image)
		self.seed = seed
		self.condition = condition
	
	def perform(self):
		print 'performing...'
		self.upLine = Line(0,self.seed,self.condition, self.im)	

class Line:
	def __init__(self, direction, seed, condition, image):
		self.direction = direction
		self.seed = seed
		self.condition = condition
		self.im = image
		print self.im.pixels[self.seed]
		translations = [
			lambda seed: seed + self.im.width,
			lambda seed: seed + 1,
			lambda seed: seed - self.im.width,
			lambda seed: seed - 1
		]
		lineLen = 0
		pxSatisfies = False
		currentPx = seed

		while pxSatisfies:
			lineLen = lineLen + 1
			currentPx = translations[direction](seed)

			pxSatisfies = condition(self.im.pixels[currentPx])
			print self.im.pixels[currentPx]
			print lineLen

		self.length = lineLen

