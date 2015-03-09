#
# BASIC SCIENCE IMAGE REDUCTION
#
import numpy as np

import Phurt.io as io


def biascombine(biasfile,writefile):
	combolist = io.read_filelist(biasfile)
	n_files = len(combolist)
	#
	# get array size (assuming all files are the same size)
	#
	img1,hdr1 = io.readimg_quik(combolist[0])
	xsize = len(img1[:,0])
	ysize = len(img1[0,:])
	filestack = np.zeros([n_files,xsize,ysize])
	i = 0
	for ff in combolist:
		filestack[i],hdr = io.readimg_quik(combolist[i])
		i += 1
	medianed = np.median(filestack, axis=0)
	if writefile!='':
		io.write_hdi(medianed,hdr,writefile)
	return medianed,hdr




def flatcombine(flatfile,masterbias,writefile):
	combolist = io.read_filelist(flatfile)
	n_files = len(combolist)
	#
	# get array size (assuming all files are the same size)
	#
	img1,hdr1 = io.readimg_quik(combolist[0])
	xsize = len(img1[:,0])
	ysize = len(img1[0,:])
	filestack = np.zeros([n_files,xsize,ysize])
	#
	# get the masterbias
	#
	masterb,hdrb = io.readimg_quik(masterbias)
	i = 0
	for ff in combolist:
		filestack[i],hdr = io.readimg_quik(combolist[i])
		filestack[i] -= masterb
		i += 1
	medianed = np.median(filestack, axis=0)
	if writefile!='':
		io.write_hdi(medianed,hdr,writefile)
	return medianed,hdr



def sciencecombine(scifi,bifi,flatfi,writefile):
	#
	# Take your masterbias, masterflat and make something out of it (single frame right now)
	#
	imgs,hdrs = io.readimg_quik(scifi)
	imgb,hdrb = io.readimg_quik(bifi)
	imgf,hdrf = io.readimg_quik(flatfi)
	mastersci = (imgs-imgb)/(imgf/np.median(imgf))
	if writefile!='':
		io.write_hdi(mastersci,hdrs,writefile)
	return mastersci,hdrs






