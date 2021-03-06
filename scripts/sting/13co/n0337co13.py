# ---------- IMPORT DATA


track_list=['C1','C2','C3','C4','C5','C6']
mirfile_list=[  'ngc337_C1_08oct24.13co.cal',
				'ngc337_C2_08oct26.13co.cal',
				'ngc337_C3_09may10.13co.cal',
				'ngc337_C4_09may12.13co.cal',
				'ngc337_C5_09may18.13co.cal',
				'ngc337_C6_09may23.13co.cal'
				]
repo='../../../../raw/co10/n0337/vis/'
telescopes=list('CARMA' for i in track_list)

for i in range(0,len(mirfile_list)):
	
	xp=xu.init()
	
	xp['rawfiles']=repo+mirfile_list[i]
	xp['prefix']=track_list[i]
	xp['importmode']='mir'
	xp['importmirarray']=telescopes[i]
	
	xp['spwrgd']			='spw'
	xp['cleanmode']		 ='velocity'
	xp['clean_start']	   ='1510km/s'
	xp['clean_nchan']	   =(1780-1510)/10+1
	xp['clean_width']	   ='10km/s'
	xp['restfreq']		  ='110.201353GHz'
	xp['outframe']		  ='LSRK'

	#xp=xu.ximport(xp)
	#xp=xu.xconsol(xp)

# ---------- IMAGE DATA

xp=xu.init()

# CONSOLIDATING 
xp['prefix']            ='../n0337/n0337co13'
xp['prefix_comb']       =track_list     

xp['spwrgd']            ='spw'
xp['freqtol']           ='0.5MHz'

# IMAGING
xp['cleanmode']         ='velocity'
xp['clean_start']       ='1510km/s'
xp['clean_nchan']       =(1780-1510)/10+1
xp['clean_width']       ='10km/s'
xp['restfreq']          ='110.201353GHz'
xp['outframe']          ='LSRK'
    
xp['phasecenter']       ='J2000 0h59m50.1 -07d34m41.00'
xp['mosweight']         =True
xp['wnpixels']          =0
xp['imsize']            =300
xp['cell']              ='1.0arcsec'

xp['minpb']             =0.05
xp['clean_mask']        ='circle[[150pix,150pix],80pix]'
xp['multiscale']        =[int(x*(2.0/0.5)) for x in [0.,1.,4.]]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0

#xu.xconsol(xp)
#xu.carmapb(xp['prefix']+'.src.ms',effdish=True)

xp['ctag']              ='_ro'
xp['cleanweight']       ='briggs'
xu.xclean(xp)
# xu.mossen(vis=xp['prefix']+'.src.ms',
#           log=xp['prefix']+xp['ctag']+'.line.sens.log',
#           nchan=xp['clean_nchan'],ftmachine='mosaic',
#           mosweight=True,imsize=xp['imsize'],
#           weight=xp['cleanweight'])


xp['ctag']              ='_na'
xp['cleanweight']       ='natural'
#xu.xclean(xp)
# xu.mossen(vis=xp['prefix']+'.src.ms',
#           log=xp['prefix']+xp['ctag']+'.line.sens.log',
#           nchan=xp['clean_nchan'],ftmachine='mosaic',
#           mosweight=True,imsize=xp['imsize'],
#           weight=xp['cleanweight'])


xp['ctag']              ='_st'
xp['cleanweight']       ='natural'
xp['multiscale']        =[]
#xu.xclean(xp)
# xu.mossen(vis=xp['prefix']+'.src.ms',
#           log=xp['prefix']+xp['ctag']+'.line.sens.log',
#           nchan=xp['clean_nchan'],ftmachine='mosaic',
#           mosweight=True,imsize=xp['imsize'],
#           weight=xp['cleanweight'])
