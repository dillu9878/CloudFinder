#!/usr/bin/env python
"""lines.py: a set of functions and classes to find the basic area of a defined space"""
__author__ = 'Max Penrose'

import coordinates, geometry

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
		print 'performing on '+str(self.seed)
		self.upLine = Line(0,self.seed,self.condition, self.im)	
		self.rightLine = Line(1,self.seed,self.condition, self.im)	
		self.downLine = Line(2,self.seed,self.condition, self.im)	
		self.leftLine = Line(3,self.seed,self.condition, self.im)	

		self.tips = []

		self.tips.append(self.upLine.tipPx)
		self.tips.append(self.rightLine.tipPx)
		self.tips.append(self.downLine.tipPx)
		self.tips.append(self.leftLine.tipPx)

		self.tipCoords = []
		
		for tip in self.tips:
			self.tipCoords.append(coordinates.Coords(tip, self.im.width))

		self.rect = geometry.rect(self.tipCoords)
		if(self.rect.area > 30):
			print 'big cloud!'

class Line:
	def __init__(self, direction, seed, condition, image):
		self.direction = direction
		self.seed = seed
		self.condition = condition
		self.im = image
		translations = [
			lambda seed: seed + self.im.width,
			lambda seed: seed + 1,
			lambda seed: seed - self.im.width,
			lambda seed: seed - 1
		]
		lineLen = 1
		pxSatisfies = True
		currentPx = seed
		tipPx = seed
		while pxSatisfies:
			currentPx = translations[direction](currentPx)
			pxSatisfies = condition(self.im.pixels[currentPx])
			if(pxSatisfies):
				tipPx = currentPx
			lineLen = lineLen + 1

		self.length = lineLen
		self.tipPx = currentPx
		print self.tipPx
