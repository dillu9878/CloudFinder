#!/usr/bin/env python
"""geometry.py: defines the shapes that can represent the area of clouds"""
__author__ = 'Max Penrose'


import numpy
import coordinates

class otherrect:
	def __init__(self, constructPoints):
		self.constructPoints = constructPoints
		self.corners = []
		# corners[] format: [top-right, bottom-right, bottom-left, top-left]
		self.corners.append(coordinates.Coords((constructPoints[1].x, constructPoints[0].y), inputType='tuple'))
		self.corners.append(coordinates.Coords((constructPoints[2].x, constructPoints[1].y), inputType='tuple'))
		self.corners.append(coordinates.Coords((constructPoints[3].x, constructPoints[2].y), inputType='tuple'))
		self.corners.append(coordinates.Coords((constructPoints[0].x, constructPoints[3].y), inputType='tuple'))

		self.width = self.corners[0].x - self.corners[3].x
		self.height = self.corners[0].y - self.corners[1].y
		self.area = self.width * self.height

	#def getPointsInside():

class rect:
	def __init__(self, img, startcorner):
		self.imgShape = img.shape
		self.TDimg = img
		self.img = img.reshape(img.size)
		self.start = startcorner

		self.imgHeight = self.imgShape[0]
		self.imgWidth = self.imgShape[1]

		self.translations = [
			lambda seed: seed + self.imgShape[1],
			lambda seed: seed + 1,
			lambda seed: seed - self.imgShape[1],
			lambda seed: seed - 1
		]
		up = 0
		right = 1
		down = 2
		left = 3

		self.bottomLeft = self.go(down)
		self.topRight = self.go(right)
		
		self.width = self.topRight - self.start
		self.height = (self.bottomLeft - self.start) // self.imgWidth

		self.topGap = self.topRight // self.imgWidth
		self.leftGap = self.topRight % self.imgWidth
		self.rightGap = self.leftGap + self.width
		self.bottomGap = self.topGap + self.height
	def go(self, direction):
		translation = self.translations[direction]
		pxIsWhite = True
		seed = self.start
		newSeed = seed
		while pxIsWhite:
			newSeed = translation(seed)
			if(self.img[seed]):
				seed = newSeed
			else:
				pxIsWhite = False

		return seed

	def getArea(self):
		return self.width * self.height

	def getPxInside(self):
		newIndexMap = numpy.arange(self.img.size).resize(self.imgHeight, self.imgWidth)
		cropped = newIndexMap[self.topGap:self.bottomGap, self.leftGap:self.rightGap]

		return pxInside


