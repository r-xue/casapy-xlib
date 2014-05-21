# ---------- B+C+D ARRAY COMBINATION 

track_list=['C1','C2','D2','D3','D4','D5','D6']
mirfile_list=['../../../../raw/co10/n3198/vis/ngc3198_C1_09apr13.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_C2_10MAR02.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_D2_09aug24.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_D3_09aug29.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_D4_09aug31.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_D5_10APR16.co.cal',
            '../../../../raw/co10/n3198/vis/ngc3198_D6_10APR21.co.cal']
telescopes=list('CARMA' for i in track_list)

for i in range(0,len(mirfile_list)):
    
    execfile(xlib+'xinit.py')
    
    xp['rawfiles']=mirfile_list[i]
    xp['prefix']=track_list[i]
    xp['importmode']='mir'
    xp['importmirarray']=telescopes[i]
    
    xp['spwrgd']            ='spw'
    xp['cleanmode']         ='velocity'
    xp['clean_start']       ='460km/s'
    xp['clean_nchan']       =(860-460)/10+1
    xp['clean_width']       ='10km/s'
    xp['restfreq']          ='115.2712GHz'
    xp['outframe']          ='LSRK'

    xp['phasecenter']       ='J2000 10h19m54.92 +45d32m59.00'

    execfile(xlib+'ximport.py')
    execfile(xlib+'xconsol.py')

  
execfile(xlib+'xinit.py')

# CONSOLIDATING 
xp['prefix']            ='n3198co'
xp['prefix_comb']       =track_list     

xp['spwrgd']             ='spw'
xp['freqtol']           ='0.5MHz'

# IMAGING
xp['cleanmode']         ='velocity'
xp['clean_start']       ='460km/s'
xp['clean_nchan']       =(860-460)/10+1
xp['clean_width']       ='10km/s'
xp['restfreq']          ='115.2712GHz'
xp['outframe']          ='LSRK'
    
xp['phasecenter']       ='J2000 10h19m54.92 +45d32m59.00'
xp['mosweight']         =True
xp['imsize']            =2**5*10
xp['cell']              ='1arcsec'

xp['multiscale']        =[0,3,9]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0
xp['minpb']             =0.10
xp['clean_mask']        =0.10

# RUN SCRIPTS
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')
xu.sumwt(xp['prefix']+'.src.ms')

