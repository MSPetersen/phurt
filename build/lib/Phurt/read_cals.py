#
# DIVIDE AND CONQUER THE CALIBRATION IMAGES
#
import numpy as np
import glob
from pkg_resources import resource_filename

import Phurt.io as io


class DivineObject(object):

    #
    # find all necessary files for reduction of given object
    #

    #
    # TODO: Throw warnings more frequently, especially if bad data is returned
    #
    
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


            self.nightdir = script_dict['nightdir']
            self.instrument = script_dict['instrument']
            self.filtername = script_dict['filtername']
            try:
                self.objectname = script_dict['objectname']
            except:
                pass
            try:
                self.rapos = [d for d in script_dict['rapos'].split(',')]
                self.decpos = [d for d in script_dict['decpos'].split(',')]
            except:
                self.rapos = script_dict['raspos']
                self.decpos = script_dict['decpos']
            self.postol = script_dict['postol']
            self.biasexclude = script_dict['masterbias']
            self.flatexclude = script_dict['masterflat']
            self.sciexclude = script_dict['finalsci']
            self.biasout = script_dict['biaslist']
            self.flatout = script_dict['flatlist']
            self.sciout = script_dict['scilist']
            
        except:
            print 'Please consider using reduce.sc to alleviate errors. No warranty for this mode (none for the other either)!'
            # prompt for values if not
            self.nightdir = raw_input("Directory to scour? ")
            self.instrument = raw_input("Which Instrument? ")
            self.filtername = raw_input("Which Filter to use? (header-compatible string) ")
            self.objectname = raw_input("Object name (ENTER if searching RA/DEC): ")
            if self.objectname=='':
                self.rapos = raw_input("Object ra (format=[rah,ram,ras]) ")
                self.decpos = raw_input("Object dec (format=[dech,decm,decs] ")
                self.postol = float(raw_input("Position Tolerance (arcsec) "))
            self.biasexclude = raw_input("Bias output file? ")
            self.flatexclude = raw_input("Flat output file? ")
            self.sciexclude = raw_input("Science output file? ")
            self.biasout = raw_input("List for biases? ")
            self.flatout = raw_input("List for flats? ")
            self.sciout = raw_input("List for science images? ")


        try:
            print 'Accepted Object name of ',self.objectname
        except:
            try:
                # check to make sure the position values are valid
                ras = self.rapos[2]
                decs = self.decpos[2]
                print 'Search position accepted:',self.rapos,self.decpos
            except:
                self.rapos = [0,0,0]
                self.decpos = [0,0,0]
                print 'RA and/or declination not recognized. Proceeding with finding calibration files ONLY...'

        # get the instrument specific values,
        #     prep for data interpretation
        self.analysislst = io.Input()
        self.analysislst.get_header_vals(resource_filename('Phurt.TScopeData',self.instrument+'.dat'))

        # should put a fancy print here for the accepted dictionary keys
        #print self.analysislst.header_names

        # break up the nightly data
        DivineObject.breaknight(self,self.nightdir)

    def on_target(self):
        self.targetstring = str(self.rapos[0])+str(self.rapos[1])+'+'+str(self.decpos[0])+str(self.decpos[1])

        try:
            if (float(self.analysislst.ras[0])==float(self.rapos[0])) & (float(self.analysislst.ras[1])==float(self.rapos[1])) & (abs(float(self.analysislst.ras[2])-float(self.rapos[2]))<=self.float(self.postol)):
                if (float(self.analysislst.dec[0])==float(self.decpos[0])) & (float(self.analysislst.dec[1])==float(self.decpos[1])) & (abs(float(self.analysislst.dec[2])-float(self.decpos[2]))<=float(self.postol)):
                    return True
            else: return False
        except: return False


    def on_name(self):
        try:
            if (self.analysislst.objn.strip()==self.objectname.strip()): return True
            else: return False
        except: return False


        

    def breaknight(self,nightdir):
        filelist = glob.glob(nightdir+'*.fits')

        biaslst = open(self.biasout,'w+')
        filterlst = open(self.flatout,'w+')
        objlst = open(self.sciout,'w+')

        for ff in filelist:
            self.analysislst.skimheaders(ff)
            if (self.analysislst.obst.strip()==self.analysislst.header_names['biases'].strip("'")) & (ff != self.biasexclude): print >>biaslst,ff
            


            if self.instrument=='HDI': # or those 'scopes with two filter wheels
                if (self.analysislst.obst.strip()==self.analysislst.header_names['flats'].strip("'")):
                    if ((self.analysislst.filters[0].strip()==self.filtername) | (self.analysislst.filters[1].strip()==self.filtername)  ) & (ff != self.flatexclude): print >>filterlst,ff
                
                if self.analysislst.obst.strip()==self.analysislst.header_names['objects'].strip("'"):
                    if ((self.analysislst.filters[0].strip()==self.filtername) | (self.analysislst.filters[1].strip()==self.filtername)  )& ( (DivineObject.on_target(self)==True) | (DivineObject.on_name(self)==True)) & (ff != self.sciexclude): print >>objlst,ff

            else:
                if (self.analysislst.obst.strip()==self.analysislst.header_names['flats'].strip("'")) & (self.analysislst.filters[0].strip()==self.filtername) & (ff != self.flatexclude): print >>filterlst,ff
                if self.analysislst.obst.strip()==self.analysislst.header_names['objects'].strip("'"):
                    if (self.analysislst.filters[0].strip()==self.filtername) & ( (DivineObject.on_target(self)==True) | (DivineObject.on_name(self)==True)) & (ff != self.sciexclude): print >>objlst,ff

        biaslst.close()
        filterlst.close()
        objlst.close()












