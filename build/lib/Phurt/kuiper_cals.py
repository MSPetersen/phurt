#
# DIVIDE AND CONQUER THE CALIBRATION IMAGES
#
import numpy as np
import glob
from pkg_resources import resource_filename

import Phurt.io as io


class PrepObject:

    #
    # find all necessary files for reduction of given object
    #

    #
    # TODO: Needs to throw warnings more frequently, especially if bad data is returned
    #
    
    def __init__(self):
        try:

            # is there a reduction script in the directory?
            script = open('reduce.sc','r')
            for line in script:
                print 'CHECKMATE! This is not built yet.'
            
        except:

            # prompt for values if not
            self.nightdir = raw_input("Directory to scour? ")
            self.instrument = raw_input("Which Instrument? ")
            self.filtername = raw_input("Which Filter to use? (header-compatible string) ")
            #self.objectname = raw_input("Object name ")
            self.rapos = raw_input("Object ra (format=[rah,ram,ras]) ")
            self.decpos = raw_input("Object dec (format=[dech,decm,decs] ")
            self.postol = float(raw_input("Position Tolerance (arcsec) "))

            try:
                x = self.rapos[2]
                y = self.decpos[2]
            except:
                print 'RA and/or declination not recognized. Proceeding with finding calibration files...'
                self.rapos = [0,0,0]
                self.decpos = [0,0,0]

        # get the instrument specific values,
        #     prep for data interpretation
        self.analysislst = io.Input()
        self.analysislst.get_header_vals(resource_filename('Phurt.TScopeData',self.instrument+'.dat'))

        print self.analysislst.header_names

        # break up the nightly data
        PrepObject.breaknight(nightdir)

    def on_target(self):
        self.targetstring = str(self.rapos[0])+str(self.rapos[1])+'+'+str(self.decpos[0])+str(self.decpos[1])
        
        if (float(self.analysislst.ras[0])==self.rapos[0]) & (float(self.analysislst.ras[1])==self.rapos[1]) & (abs(float(self.analysislst.ras[2])-self.rapos[2])<=self.postol):
    		if (float(self.analysislst.des[0])==self.decpos[0]) & (float(self.analysislst.des[1])==self.decpos[1]) & (abs(float(self.analysislst.des[2])-self.decpos[2])<=self.postol):
    			return True
        else: return False


    def breaknight(self,nightdir):
        filelist = glob.glob(nightdir+'*.fits')

        biaslst = open(nightdir+'bias.list','w+')
        filterlst = open(nightdir+self.filtername.strip(),'w+')
        objlst = open(nightdir+self.objectname.strip(),'w+')

        for ff in filelist:
            self.analysislst.skimheaders(ff)
            if (self.obst.strip()==self.analysislst.header_names['biases']): print >>biasl,ff
            if (self.obst.strip()==self.analysislst.header_names['flats']) & (self.filters[0].strip()==self.filtername): print >>filterlst,ff

            try:
                if (self.obst.strip()==self.analysislst.header_names['objects']) & ((self.filters[0].strip()==self.filtername) | (self.filters[1].strip()==self.filtername)  )& (on_target()==True): print >>objlst,ff

            except:
                if (self.obst.strip()==self.analysislst.header_names['objects']) & (self.filters[0].strip()==self.filtername) & (on_target()==True): print >>objlst,ff












