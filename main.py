from PIL import Image
import sys
import time
import lines, colours

startTime = time.time()

imPath = sys.argv[1]

im = Image.open(imPath).convert('RGBA')
#im.show()

pixel = list(im.getdata())

# main looooooop

for pxref, px in enumerate(im.getdata()):
	if(colours.testIsWhite(px)): 
		lines.LineSpaceFinder(pxref, colours.testIsWhite, im).perform()



'''
matrix = ( r / 255.0, 0.0, 0.0, 0.0, 0.0, g / 255.0, 0.0, 0.0, 0.0, 0.0, b / 255.0, 0.0 )
im.convert('RGBA', matrix).show()
'''
# Image.eval(im, lambda px: 0 if px < 150 else px).show()

finTime = time.time()
runTime = finTime - startTime
print 'Program completed in '+str(runTime)+' secs'
