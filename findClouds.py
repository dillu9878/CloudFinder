#!/usr/bin/env python

#from PIL import Image
import numpy
import sets
import sys
import os
import cStringIO
import argparse

from osgeo import gdal, gdal_array

from planet_common.client import urls, storage

class rect:
	def __init__(self, img, startcorner, checkedpxs):
		self.imgShape = img.shape
		self.TDimg = img
		self.img = img.reshape(img.size)
		self.start = startcorner
		self.checkedpxs = checkedpxs

		self.imgHeight = self.imgShape[0]
		self.imgWidth = self.imgShape[1]

		self.translations = [
			lambda seed: seed - self.imgWidth,
			lambda seed: seed + 1,
			lambda seed: seed + self.imgWidth,
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

	def go(self, direction):
		translation = self.translations[direction]
		pxIsWhite = True
		seed = self.start
		newSeed = seed
		while pxIsWhite:
			newSeed = translation(seed)
			if(int(seed) in self.checkedpxs):
				pxIsWhite = False
			elif(self.img[seed]):
				seed = newSeed
			else:
				pxIsWhite = False
		return seed

	def getArea(self):
		area = self.width * self.height
		if(area < 30):
			return 0
		else:
			return area
	def getPxInside(self):
		cropped = []

		for sub_start in range(self.start, self.bottomLeft, self.imgWidth):

			cropped += range(sub_start, sub_start+self.width)

		return cropped

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
	isWhite = numpy.logical_and(rangeOK, meanOK)

	return isWhite


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

def main(args):
	print 'main'
	imPath = args.input_file

	imFilePath = storage.get_scene_file(None, 'flock1_pretty', imPath)

	#im = Image.open(imFilePath)
	#pxArray = numpy.asarray(im)

	pxArray = gdal_array.LoadFile(imFilePath)

	#pxArray = numpy.array(im.getdata()).reshape(im.size[0], im.size[1], 4)


	darknessArray = cleanNoiseNP(testIsWhiteNP(pxArray))

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
			currentRect = rect(darknessArray, index, usedPixels)
			usedPixels = usedPixels.union(sets.Set(currentRect.getPxInside()))
			cloudCover += currentRect.getArea()


	cloudCoverPercent = (float(cloudCover) / float(darknessArray.size)) * 1000

	print 'the cloud cover is at ' + str(cloudCoverPercent) + '%'


def RunFromArgs(rawargs):
    aparser = argparse.ArgumentParser(
        description='Search for and find the area of the image obscured by cloud')

    aparser.add_argument('-c', '--cloud',
                         help='services domain, ie athq.pl or raxpl.us')
    aparser.add_argument('--info', action='store_true',
                         help='Turn on INFO level logging.')
    aparser.add_argument('--debug', action='store_true',
                         help='Turn on DEBUG level logging.')
    aparser.add_argument('input_file')

    args = aparser.parse_args(rawargs[1:])

    if args.cloud:
        urls.set_urls(args.cloud)

    main(args)

def RunFromEnv():
    args = [sys.argv[0]]

    if 'INPUT_FILE' in os.environ:
        args += os.environ['INPUT_FILE']

    if 'CMD_OPTS' in os.environ:
        args += os.environ['CMD_OPTS'].split()

    logging.info('Invoking with arguments:\n  %s' % ' '.join(args))
    RunFromArgs(args)


if __name__ == '__main__':
    if len(sys.argv) == 1 and 'PL_JOB_ID' in os.environ:
        status = RunFromEnv()
    else:
        status = RunFromArgs(sys.argv)

    sys.exit(status)
