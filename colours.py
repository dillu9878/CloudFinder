#!/usr/bin/env python
"""colours.py: the testers file"""
__author__ = 'Max Penrose'
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