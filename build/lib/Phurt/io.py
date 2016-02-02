#
# IO for reading HDI images and reduced versions
#
import numpy as np
from astropy.io import fits
from astropy.io.fits import getheader
import glob


class Input():

    #
    # class to handle inputs, now constructed to make fewer changes elsewhere
    #
    
    def get_header_vals(self,tel_data):
        """

        Returns a dictionary of the instrument-specific quantities/header values

        """
        self.header_names = {}
        
        f = open(tel_data)
        for line in f:
            q = [d for d in line.split('=')]
            self.header_names[q[0].strip()] = q[1].strip()


    def skimheaders(self,infile):
        #
        # accept telemetry card as a variable?
        #
        cc = fits.open(infile)
        self.obst = cc[0].header[self.header_names['obs_type']]
        self.expt = cc[0].header[self.header_names['exp_time']]
        # object name to go here...
        self.objn = cc[0].header[self.header_names['object_title']]

        #
        # guards against multiple filter wheels (needed for HDI data)
        #
        try: self.filters = [cc[0].header[self.header_names['filter1']],cc[0].header[self.header_names['filter2']]]
        except: self.filters = cc[0].header[self.header_names['filter1']]

        
        if self.header_names['posflag'] == 'SEXIGESIMAL':
            rast = cc[0].header[self.header_names['rastring']]
            self.ras = [q.strip('+') for q in rast.split(':')]
            dect = cc[0].header[self.header_names['decstring']]
            self.dec = [q.strip('+') for q in dect.split(':')]
        else:
            self.ras = cc[0].header[self.header_names['rastring']]
            self.dec = cc[0].header[self.header_names['dectring']]
        self.tval = cc[0].header[self.header_names['ut_time']]
        return self.obst,self.expt,self.filters,self.ras,self.dec,self.tval,self.objn



class ImageRead():
    
    def get_header_vals(self,tel_data):
        """

        Returns a dictionary of the instrument-specific quantities/header values

        """
        self.header_names = {}
        
        f = open(tel_data)
        for line in f:
            q = [d for d in line.split('=')]
            self.header_names[q[0].strip()] = q[1].strip()


    def trim_image(self,img):  return img[0:int(self.header_names['good_x']),0:int(self.header_names['good_y'])]




    def readimg_quik(self,infile):
        # READ IN IMAGES QUICKLY/DIRTILY
        #     subtract off overscan region if not already done?
        self.data,self.hdr0 = fits.getdata(infile,header=True)
        try:
            self.hdr1 = fits.getheader(infile,1)
            self.phdr = fits.getheader(infile,0)
            print infile,'...Reading Card 1...'
        except: 
            print infile,'...Reading Header Card 0...'
            self.phdr = self.hdr0
        self.imgout = ImageRead.trim_image(self,self.data)
        return self.imgout,self.phdr



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


	
def write_new_fits(data,hdr,outfile):

    #
    # might be fun to have an option for lighter/heavier formats...currently set to write 16-bit floats (OUCH).
    #
    
    dataf = [[float(val) for val in inner] for inner in data]
    dataarr = np.array(data, dtype=np.float32)
    #fits.writeto(outfile,dataf,hdr,clobber=True)
    fits.writeto(outfile,dataarr,hdr,clobber=True)

	
	


