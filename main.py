from PIL import Image, ImageEnhance
import sys
import time
import pixelclumps

startTime = time.time()

imPath = sys.argv[1]

im = Image.open(imPath).convert('RGBA')
#im.show()

pixels = list(im.getdata())

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

pxref = 0

testIsWhite((200,200,200))
# main looooooop

for RGBA in pixels:
	if(i in pixelclumps.cleanedAreas):
		if(testIsWhite(RGBA)):
			pixelclumps.findClumps(im, pxref, testIsWhite)

	pxref=pxref+1



'''
matrix = ( r / 255.0, 0.0, 0.0, 0.0, 0.0, g / 255.0, 0.0, 0.0, 0.0, 0.0, b / 255.0, 0.0 )
im.convert('RGBA', matrix).show()
'''
# Image.eval(im, lambda px: 0 if px < 150 else px).show()

finTime = time.time()
runTime = finTime - startTime
print 'Program completed in '+str(runTime)+' secs'
