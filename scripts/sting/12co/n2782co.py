# ---------- B+C+D ARRAY COMBINATION 

track_list=['C1','C2','C3','C4']
mirfile_list=['../../../../raw/co10/n2782/vis/ngc2782_C1_08may19.co.cal',
            '../../../../raw/co10/n2782/vis/ngc2782_C2_08may31.co.cal',
            '../../../../raw/co10/n2782/vis/ngc2782_C3_08jun01.co.cal',
            '../../../../raw/co10/n2782/vis/ngc2782_C4_08jun03.co.cal']
telescopes=list('CARMA' for i in track_list)

for i in range(0,len(mirfile_list)):

    xp=xu.init()
    
    xp['rawfiles']=mirfile_list[i]
    xp['prefix']=track_list[i]
    xp['importmode']='mir'
    xp['importmirarray']=telescopes[i]
    
    xp['spwrgd']            ='spw'
    xp['cleanmode']         ='velocity'
    xp['clean_start']       ='2410km/s'
    xp['clean_nchan']       =(2670-2410)/10+1
    xp['clean_width']       ='10km/s'
    xp['restfreq']          ='115.2712GHz'
    xp['outframe']          ='LSRK'

    xp['phasecenter']       ='J2000 09h14m05.10 40d06m49.00'

    #xp=xu.ximport(xp)
    #xp=xu.xconsol(xp)

xp=xu.init()

# CONSOLIDATING 
xp['prefix']            ='../n2782/n2782co'
xp['prefix_comb']       =track_list     

xp['spwrgd']             ='spw'
xp['freqtol']           ='0.5MHz'

# IMAGING
xp['cleanmode']         ='velocity'
xp['clean_start']       ='2410km/s'
xp['clean_nchan']       =(2670-2410)/10+1
xp['clean_width']       ='10km/s'
xp['restfreq']          ='115.2712GHz'
xp['outframe']          ='LSRK'
    
xp['phasecenter']       ='J2000 09h14m05.10 40d06m49.00'
xp['mosweight']         =True
xp['wnpixels']          =0
xp['imsize']            =600
xp['cell']              ='0.5arcsec'

xp['minpb']             =0.05
xp['clean_mask']        =0.25
xp['multiscale']        =[int(x*(1.5/0.5)) for x in [0.,1.,3.]]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0


# RUN SCRIPTS

# xu.xconsol(xp)
# xu.carmapb(xp['prefix']+'.src.ms',effdish=True)

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
# 
# execfile(xlib+'xconsol.py')
# execfile(xlib+'xclean.py')
# xu.sumwt(xp['prefix']+'.src.ms')