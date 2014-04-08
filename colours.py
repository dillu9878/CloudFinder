#!/usr/bin/env python
"""colours.py: the testers file"""
__author__ = 'Max Penrose'

import numpy

def testIsWhite(RGBA):
	pxIsWhite = True
	RGB = RGBA[:3]

	RGBl = 255
	RGBu = 0

	RGBsum = 0

	for colour in RGB:
		if(RGBl > colour):
			RGBl = colour
		
		if(RGBu < colour):
			RGBu = colour
	
		RGBsum = RGBsum + colour
	
	RGBrange = RGBu - RGBl
	RGBmean = RGBsum / 3 

	if(RGBrange > 10 or RGBmean < 145):
		pxIsWhite = False

	return pxIsWhite

def testSurroundsAreWhite(img, seed):

	# surrounds format: numpy.array([top,right,bottom,left])
	surrounds = numpy.zeros((1, 4))
	surrounds[0] = img[seed[0]+1,seed[1]]
	surrounds[1] = img[seed[0],seed[1]+1]
	surrounds[2] = img[seed[0]-1,seed[1]]
	surrounds[3] = img[seed[0],seed[1]-1]

	return testIsWhiteNP(surrounds)

def cleanNoiseNP(img):
	leftSide = img[1:-1,0:-2]
	topSide = img[0:-2,1:-1]
	rightSide = img[1:-1,2:]
	bottomSide = img[2:,1:-1]

	thisPx = img[1:-1,1:-1]
	
	result = numpy.logical_and(
		numpy.logical_and(
			numpy.where(leftSide,thisPx,False),
			numpy.where(rightSide, thisPx, False)
		),
		numpy.logical_and(
			numpy.where(topSide, thisPx, False),
			numpy.where(bottomSide, thisPx, False)
		)
	)
	return result

def testIsWhiteNP(img):
	imgMin = numpy.minimum (
		numpy.minimum(img[:,:,0],img[:,:,1]),
		img[:,:,2]
	)

	imgMax = numpy.maximum (
		numpy.maximum(img[:,:,0],img[:,:,1]),
		img[:,:,2]
	)

	imgRange = imgMax - imgMin

	imgSum = img[:,:,0].astype(numpy.int16) + img[:,:,1] + img[:,:,2]
	imgMean = imgSum/3

	rangeOK = numpy.less(imgRange,10)

	meanOK = numpy.greater(imgMean, 145)
	print numpy.count_nonzero(meanOK)
	isWhite = numpy.logical_and(rangeOK, meanOK)

	return isWhite
