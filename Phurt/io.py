#
# IO for reading HDI images and reduced versions
#
import numpy as np
from astropy.io import fits
from astropy.io.fits import getheader
import glob
import matplotlib.pyplot as plt



def skimheaders(infile):
    # SKIM HEADERS, VERY DIRTILITY
    cc = fits.open(infile)
    obst = cc[0].header['OBSTYPE']
    expt = cc[0].header['EXPTIME']
    filters = [cc[0].header['FILTER1'],cc[0].header['FILTER2']]
    rast = cc[0].header['RASTRNG']
    ras = [q.strip('+') for q in rast.split(':')]
    dect = cc[0].header['DECSTRNG']
    dec = [q.strip('+') for q in dect.split(':')]
    tval = cc[0].header['DATE-OBS']
    return obst,expt,filters,ras,dec,tval


# TRIM HDI IMAGES TO A GOOD VALUE
def trim_image(img,xdead,ydead):  return img[0:xdead,0:ydead]


xdead = 4112
ydead = 4096




def readimg_quik(infile):
	# READ IN HDI IMAGES QUICKLY/DIRTILY
	#     subtract off overscan region if not already done
  	data,hdr0 = fits.getdata(infile,header=True)
    	try: 
    		# check to see if this is an original HDI file, if so, get original telemetry header
    		hdr1 = fits.getheader(infile,1)
    		phdr = fits.getheader(infile,0)
    	except: 
    		print 'This is not an original HDI file!'
    		phdr = hdr0
    	imgout = trim_image(data,xdead,ydead)
    	return imgout,phdr



def read_filelist(infile):
	#
	# read in file lists
	# 
	filelist = []
	f = open(infile)
	for line in f:
		filelist.append(line)
	f.close()
	return np.array(filelist)


	
def write_hdi(data,hdr,outfile):
	#
	# cleanly write to 
	#
	fits.writeto(outfile,data,hdr,clobber=True)
	
	


