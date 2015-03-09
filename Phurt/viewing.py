#
# interface with ds9 to display the image
#      MUST have 'ds9' be a valid command line alias
#

import subprocess


def dsdisplay(imagefile):
	callstring = 'ds9 '+imagefile+' &'
	subprocess.call([callstring],shell=True)
