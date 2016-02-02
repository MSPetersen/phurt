#
# BASIC SCIENCE IMAGE REDUCTION
#
import numpy as np
from pkg_resources import resource_filename


import Phurt.io as io


class ReduceObject: # can this handle a script input? this would probably be the best spot to put it.

    def __init__(self,inscript):
        try:

            # is there a reduction script in the directory?
            script = open(inscript)
            #script = open('/Users/MSP/reduce.sc')
            script_dict = {}
            for line in script:
                try:
                    q = [d for d in line.split('=')]
                    script_dict[q[0].strip()] = q[1].strip()
                except: pass
            
            self.biasfile = script_dict['masterbias']
            self.flatfile = script_dict['masterflat']
            self.scifile = script_dict['finalsci']
            self.objectname = script_dict['objectname']
            self.biaslist = script_dict['biaslist']
            self.flatlist = script_dict['flatlist']
            self.scilist = script_dict['scilist']
            self.instrument = script_dict['instrument']

        except:
            print 'Reduction script (reduce.sc) required to run.'
            

    def biascombine(self,writeflag):
        print 'Bias Combination...'
        combolist = io.read_filelist(self.biaslist)
        #print 'Files accepted:',combolist
        n_files = len(combolist)
        self.IMG = io.ImageRead()
        self.IMG.get_header_vals(resource_filename('Phurt.TScopeData',self.instrument+'.dat'))
        #
        # get array size (assuming all files are the same size)
        #
        self.img1,self.hdr1 = self.IMG.readimg_quik(combolist[0].strip())
        xsize = len(self.img1[:,0])
        ysize = len(self.img1[0,:])
        filestack = np.zeros([n_files,xsize,ysize])
        i = 0
        for ff in combolist:
            filestack[i],hdr = self.IMG.readimg_quik(combolist[i].strip())
            i += 1
        self.medianed = np.median(filestack, axis=0)
        if writeflag!=0:
            io.write_new_fits(self.medianed,self.hdr1,self.biasfile)
        #return medianed,hdr




    def flatcombine(self,writeflag):
        print 'Flat combination...'
        combolist = io.read_filelist(self.flatlist)
        n_files = len(combolist)
        self.IMG = io.ImageRead()
        self.IMG.get_header_vals(resource_filename('Phurt.TScopeData',self.instrument+'.dat'))
        self.img1,self.hdr1 = self.IMG.readimg_quik(combolist[0].strip())
        xsize = len(self.img1[:,0])
        ysize = len(self.img1[0,:])
        filestack = np.zeros([n_files,xsize,ysize])
        #
        # get the masterbias
        #
        self.imgb,self.hdrb = self.IMG.readimg_quik(self.biasfile)
        i = 0
        for ff in combolist:
            filestack[i],self.hdr = self.IMG.readimg_quik(combolist[i].strip())
            filestack[i] -= self.imgb
            i += 1
        self.medianed = np.median(filestack, axis=0)
        if writeflag!='':
            io.write_new_fits(self.medianed,self.hdr,self.flatfile)
        #return medianed,hdr


    def sciencecombine(self,writeflag,stackflag,normalflag):
        print 'Science combination...'
        combolist = io.read_filelist(self.scilist)
        n_files = len(combolist)
        self.IMG = io.ImageRead()
        self.IMG.get_header_vals(resource_filename('Phurt.TScopeData',self.instrument+'.dat'))
        self.img1,self.hdr1 = self.IMG.readimg_quik(combolist[0].strip())
        #
        # Take your masterbias, masterflat and make something out of it
        #
        xsize = len(self.img1[:,0])
        ysize = len(self.img1[0,:])
        filestack = np.zeros([n_files,xsize,ysize])
        #
        # get the masterbias
        #
        self.imgb,self.hdrb = self.IMG.readimg_quik(self.biasfile)
        self.imgf,self.hdrf = self.IMG.readimg_quik(self.flatfile)
        i = 0
        for ff in combolist:
            filestack[i],self.hdr = self.IMG.readimg_quik(combolist[i].strip())     # read in the science image
            filestack[i] -= self.imgb                                               # remove the bias
            filestack[i] /= (self.imgf/np.median(self.imgf))                        # normalize by the flatfield
            if normalflag:
                filestack[i] /= self.hdr['EXPTIME']     # normalize for time--this needs to be adapted to be the instrument data
            if not stackflag:
                last_dot = ff.rfind('.')
                newfilename = ff[0:last_dot]+'_red.fits'
                io.write_new_fits(filestack[i],self.hdr,newfilename)
                print 'New reduced science file made:',newfilename
            i += 1
        self.medianed = np.median(filestack, axis=0)                                # this step is painfully slow

        if writeflag!=False:
            io.write_new_fits(self.medianed,self.hdr,self.scifile)
        #return mastersci,hdrs




def run_all(inscript):
    
    fullobj = ReduceObject(inscript)
    fullobj.biascombine(True)
    fullobj.flatcombine(True)

    #
    # Note that if you already have the bias and flat created, you can execute just the ReduceObject() initialization, then this sciencecombine step.
    #
    fullobj.sciencecombine(True,stackflag=True,normalflag=False)

