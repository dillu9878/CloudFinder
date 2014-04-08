from PIL import Image
import numpy
import sets
import sys
import time
import lines, colours, coordinates, geometry

startTime = time.time()

imPath = sys.argv[1]
print 'about to open'
im = Image.open(imPath)
#im.show()
print 'opened'
#pixel = list(im.getdata())

pxArray = numpy.asarray(im)

#pxArray = numpy.array(im.getdata()).reshape(im.size[0], im.size[1], 4)


darknessArray = colours.cleanNoiseNP(colours.testIsWhiteNP(pxArray))

fullIndexArray = numpy.where(darknessArray.reshape((darknessArray.size)), 
	numpy.arange(darknessArray.size), 
	numpy.ones(darknessArray.size, dtype=numpy.int64)*-1
)

indexesOfNegatives = numpy.argwhere(
	fullIndexArray<0
)

indexesOfNegatives.shape = (indexesOfNegatives.size)

cleanIndexArray = numpy.delete(fullIndexArray, indexesOfNegatives)

usedPixels = sets.Set()
cloudCover = 0

print cleanIndexArray.shape

for index in numpy.nditer(cleanIndexArray):
	if(int(index) not in usedPixels):
		print len(usedPixels), '/', cleanIndexArray.size
		currentRect = geometry.rect(darknessArray, index, usedPixels)
		print currentRect.getPxInside().tolist()[0]
		usedPixels = usedPixels.union(sets.Set(currentRect.getPxInside().tolist()[0]))
		cloudCover += currentRect.getArea()
	else:
		print 'skipping...'

cloudCoverPercent = (cloudCover / darknessArray.size) * 1000

print 'the cloud cover is at ' + str(cloudCoverPercent) + '%'

finTime = time.time()
runTime = finTime - startTime
print 'Program completed in '+str(runTime)+' secs'
