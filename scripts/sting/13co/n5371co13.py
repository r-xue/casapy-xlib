# ---------- B+C+D ARRAY COMBINATION 

track_list=['C1','C2','C3','C4','C5','D1','D2','D3','D4','D5','D6']
mirfile_list=[	'../../../../raw/co10/n5371/vis/ngc5371_C1_09may11.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_C2_09may12.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_C3_09may13.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_C4_09may14.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_C5_09may18.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D1_10APR16.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D2_10APR17.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D3_10APR18.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D4_10APR21.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D5_10MAY06.13co.cal',
				'../../../../raw/co10/n5371/vis/ngc5371_D6_10MAY11.13co.cal']
telescopes=list('CARMA' for i in track_list)

for i in range(0,len(mirfile_list)):

	xp=xu.init()
	
	xp['rawfiles']=mirfile_list[i]
	xp['prefix']=track_list[i]
	xp['importmode']='mir'
	xp['importmirarray']=telescopes[i]
	
	xp['spwrgd']			='spw'
	xp['cleanmode']		 ='velocity'
	xp['clean_start']	   ='2360km/s'
	xp['clean_nchan']	   =(2750-2360)/10+1
	xp['clean_width']	   ='10km/s'
	xp['restfreq']		  ='110.201353GHz'
	xp['outframe']		  ='LSRK'

# 	xp=xu.ximport(xp)
# 	xp=xu.xconsol(xp)

xp=xu.init()
 
# CONSOLIDATING 
xp['prefix']            ='../n5371/n5371co13'
xp['prefix_comb']       =track_list     
 
xp['spwrgd']             ='spw'
xp['freqtol']           ='0.5MHz'
 
# IMAGING
xp['cleanmode']		 ='velocity'
xp['clean_start']	   ='2360km/s'
xp['clean_nchan']	   =(2750-2360)/10+1
xp['clean_width']	   ='10km/s'
xp['restfreq']		  ='110.201353GHz'
xp['outframe']		  ='LSRK'

xp['phasecenter']       ='J2000 13h55m39.9 +40d27m41.99'
xp['mosweight']         =True
xp['wnpixels']          =0
xp['imsize']            =320
xp['cell']              ='1.0arcsec'

xp['minpb']             =0.05
xp['clean_mask']        =0.20
xp['multiscale']        =[int(x*(2.5/1.0)) for x in [0.,1.,4.]]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0

# xu.xconsol(xp)
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
#os.system('cp -rf '+xp['prefix']+'_na.line.sens.log '+xp['prefix']+'_st.line.sens.log')
