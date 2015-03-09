"""
Getting started with P-HURT

Build the python files in the traditional way

$ cd Phurt
$ python setup.py install

Then in python:

>>> import Phurt

Break up a night into the constituent observations

>>> import Phurt.id_cals
>>> nightdir = '/home/mpetersen/WIYNDATA/jan19/'
>>> Phurt.id_cals.breaknight(nightdir)

This will create several files in the chosen directory that can then be fed to Phurt.
The flat nomenclature is w[wheelnumber]f[filternumber].list, such that wheel 1, filter 0 is w1f0.list
The bias nomenclature is bias.list

These will come out in whatever directory the data is stored in.

To get the data for a specific object, use

>>> ra = [01, 32, 14] # the ra string
>>> dec = [28, 53, 57] # the dec string
>>> tol = 60 # the tolerance for pointing, in arcsec
>>> filter = 100 # the filter, in HDI-speak
>>> id_cals.findobject(nightdir,ra,dec,tol,filter)

This will make a list labeled with the coordinates (here it spits out '132+2853.list' in nightdir) 

>>> import Phurt.io
>>> Phurt.io.read_filelist(nightdir+'w1f0.list')

Make a median combined version of the flats (must do biases first, which follows the same idea--see below)
NOTE: This currently allows you to do stupid things with memory allocation, so it can get very broken. Probably don't try this on filelists of more than 8 files (especially not on my shitty 2 GB computer).

>>> import Phurt.reduce
>>> comb_img,hdr = Phurt.reduce.flatcombine(nightdir+'w1f0.list','')


Write the file out (including the header!)

>>> Phurt.io.write_hdi(comb_img,hdr,nightdir+'w1f0flat.fits')


View the file
NOTE: This requires that ds9 be a command-line-callable option. Otherwise, do it the old-fashioned way with a point and click.

>>> import Phurt.viewing
>>> Phurt.viewing.dsdisplay(nightdir+'w1f0flat.fits')



For those keeping score at home, here's the full script (Note that this whole page is run-able!)

I tested everything below here and it worked on my machine, so let me know if anything breaks for you...

"""


import Phurt
import Phurt.id_cals
import Phurt.io
import Phurt.reduce
import Phurt.viewing

nightdir = '/home/mpetersen/WIYNDATA/jan19/'
Phurt.id_cals.breaknight(nightdir)

ra = [01, 32, 14] # the ra string
dec = [28, 53, 57] # the dec string
tol = 60 # the tolerance for pointing, in arcsec
filter = 105 # the filter, in HDI-speak
Phurt.id_cals.findobject(nightdir,ra,dec,tol,filter)

# bias stuff

comb_bias,hdr = Phurt.reduce.biascombine(nightdir+'bias.list',nightdir+'masterbias.fits')

# flat stuff

comb_flat,hdr = Phurt.reduce.flatcombine(nightdir+'w1f0.list',nightdir+'masterbias.fits',nightdir+'w1f0masterflat.fits')


# science images?!

scifis = Phurt.io.read_filelist(nightdir+'132+2853.list')

Phurt.reduce.sciencecombine(scifis[0],nightdir+'masterbias.fits',nightdir+'w1f0masterflat.fits',nightdir+'scitest.fits')












