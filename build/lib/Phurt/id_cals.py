#
# DIVIDE AND CONQUER THE CALIBRATION IMAGES
#
import numpy as np
from astropy.io import fits
from astropy.io.fits import getheader
import glob
import matplotlib.pyplot as plt


import Phurt.io as io


def breaknight(nightdir):
	#nightdir = '/home/mpetersen/WIYNDATA/jan19/*.fits'
	filelist = glob.glob(nightdir+'*.fits')
	
	#
	# predicated on knowledge that HDI has 2 8-filter wheels
	#
	
	#
	# initialize files
	# 
	biasl = open(nightdir+'bias.list','w+')
	w1f0 = open(nightdir+'w1f0.list','w+')
	w1f1 = open(nightdir+'w1f1.list','w+')
	w1f2 = open(nightdir+'w1f2.list','w+')
	w1f3 = open(nightdir+'w1f3.list','w+')
	w1f4 = open(nightdir+'w1f4.list','w+')
	w1f5 = open(nightdir+'w1f5.list','w+')
	w1f6 = open(nightdir+'w1f6.list','w+')
	w1f7 = open(nightdir+'w1f7.list','w+')
	w2f0 = open(nightdir+'w2f0.list','w+')
	w2f1 = open(nightdir+'w2f1.list','w+')
	w2f2 = open(nightdir+'w2f2.list','w+')
	w2f3 = open(nightdir+'w2f3.list','w+')
	w2f4 = open(nightdir+'w2f4.list','w+')
	w2f5 = open(nightdir+'w2f5.list','w+')
	w2f6 = open(nightdir+'w2f6.list','w+')
	w2f7 = open(nightdir+'w2f7.list','w+')

	for ff in filelist:
    		obst,expt,filters,ras,dec,tval = io.skimheaders(ff)
		if (obst=='BIAS'): print >>biasl,ff
    		if (obst=='FLAT') & (filters[0]=='100'): print >>w1f0,ff
    		if (obst=='FLAT') & (filters[0]=='101'): print >>w1f1,ff
    		if (obst=='FLAT') & (filters[0]=='102'): print >>w1f2,ff
    		if (obst=='FLAT') & (filters[0]=='103'): print >>w1f3,ff
    		if (obst=='FLAT') & (filters[0]=='104'): print >>w1f4,ff
    		if (obst=='FLAT') & (filters[0]=='105'): print >>w1f5,ff
    		if (obst=='FLAT') & (filters[0]=='106'): print >>w1f6,ff
    		if (obst=='FLAT') & (filters[0]=='107'): print >>w1f7,ff
    		if (obst=='FLAT') & (filters[1]=='200'): print >>w2f0,ff
    		if (obst=='FLAT') & (filters[1]=='201'): print >>w2f1,ff
    		if (obst=='FLAT') & (filters[1]=='202'): print >>w2f2,ff
    		if (obst=='FLAT') & (filters[1]=='203'): print >>w2f3,ff
    		if (obst=='FLAT') & (filters[1]=='204'): print >>w2f4,ff
    		if (obst=='FLAT') & (filters[1]=='205'): print >>w2f5,ff
    		if (obst=='FLAT') & (filters[1]=='206'): print >>w2f6,ff
    		if (obst=='FLAT') & (filters[1]=='207'): print >>w2f7,ff





def findobject(nightdir,ra,dec,tol,filt):
	# RA in [rahours,ramin,rasec]
	# DEC in [dechours,decmin,decsec]
	# tol in arcsecs
	# filt in HDI-speak (e.g. '100')
	
	#
	# This is not very pretty.
	# 
	filelist = glob.glob(nightdir+'*.fits')
	targetstring = str(ra[0])+str(ra[1])+'+'+str(dec[0])+str(dec[1])
	targetlist = open(nightdir+targetstring+'.list','w+')
	for ff in filelist:
    		obst,expt,filters,ras,des,tval = io.skimheaders(ff)
    		if (obst=='OBJECT') & ((filters[0]==str(filt)) | (filters[1] == str(filt))): 
    			if (float(ras[0])==ra[0]) & (float(ras[1])==ra[1]) & (abs(float(ras[2])-ra[2])<=tol):
    				if (float(des[0])==dec[0]) & (float(des[1])==dec[1]) & (abs(float(des[2])-dec[2])<=tol):
    					print >>targetlist,ff










