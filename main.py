from PIL import Image
import numpy
import sys
import time
import lines, colours, coordinates

startTime = time.time()

imPath = sys.argv[1]
print 'about to open'
im = Image.open(imPath)
#im.show()
print 'opened'
#pixel = list(im.getdata())

pxArray = numpy.asarray(im)

#pxArray = numpy.array(im.getdata()).reshape(im.size[0], im.size[1], 4)


imgIsWhite = colours.cleanNoiseNP(colours.testIsWhiteNP(pxArray))

BaWmask = numpy.where(imgIsWhite,255,0).astype(numpy.uint8)

print BaWmask.shape
print BaWmask.dtype
print numpy.count_nonzero(imgIsWhite)
resultImage = Image.fromarray(BaWmask)

resultImage.save('/Users/planetlabs/Desktop/BaWCLEAN.tif')

# main looooooop
"""
for pxref, px in enumerate(im.getdata()):
	if(colours.testIsWhite(px)): 
		lines.LineSpaceFinder(pxref, colours.testIsWhite, im).perform()
"""


'''
matrix = ( r / 255.0, 0.0, 0.0, 0.0, 0.0, g / 255.0, 0.0, 0.0, 0.0, 0.0, b / 255.0, 0.0 )
im.convert('RGBA', matrix).show()
'''
# Image.eval(im, lambda px: 0 if px < 150 else px).show()

finTime = time.time()
runTime = finTime - startTime
print 'Program completed in '+str(runTime)+' secs'
