from PIL import Image
import numpy
import sets
import sys
import time
import cStringIO
import colours, geometry

startTime = time.time()

imPath = sys.argv[1]
print 'about to open'
im = Image.open(imPath)
#im.show()
print 'opened'
#pixel = list(im.getdata())

url = 'https://storage.planet-labs.com/v0/scenes/flock1_rectified/20140219_220641_073c_r.tif/raw'

def authFetch(url):
    """
    Some versions of the requests library have trouble following a redirect
    from an url with userid/password without passing it on the redirect too.
    This function helps us work around that using urllib2.  A proper fix
    is already upstream in requests, and has made it into our 12.04 repos.
    """

    

    import urllib2
    passman =  urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, 'https://storage.planet-labs.com',
                     'cosmogia', 'pieppiep')
    urllib2.install_opener(
        urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    rv = urllib2.urlopen(url)
    return rv


#print authFetch(url).read()
#imfile = cStringIO.StringIO(authFetch(url).read())

#im = Image.open(imfile)


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

for index in numpy.nditer(cleanIndexArray):
	if(int(index) not in usedPixels):
		currentRect = geometry.rect(darknessArray, index, usedPixels)
		usedPixels = usedPixels.union(sets.Set(currentRect.getPxInside()))
		cloudCover += currentRect.getArea()


cloudCoverPercent = (float(cloudCover) / float(darknessArray.size)) * 100

print 'the cloud cover is at ' + str(cloudCoverPercent) + '%'

finTime = time.time()
runTime = finTime - startTime
print 'Program completed in '+str(runTime)+' secs'
