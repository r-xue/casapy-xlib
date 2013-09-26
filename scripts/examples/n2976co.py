track_list=['bima'+str(i+1) for i in range(24)]+['C'+str(i+1) for i in range(8)]
telescopes=['bima']*24+['CARMA']*8

mirfile_list= [ '../../sting-co/sdi/bima/n2976/n2976/old/n2976.1.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976/old/n2976.2.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01apr01/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01apr30/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01may02/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01may08/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01may27/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01jun02/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976_C/01jun04/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/n2976/01jun21/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976/01jun23/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976_B/02feb26/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976_B/02mar02/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976_B/02mar03/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976_B/02mar04/n2976.usb',
                '../../sting-co/sdi/bima/n2976/n2976_B/02mar08/n2976.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976n/03may20.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976n/03may12.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976n/03may14.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/d115.2976n/03jun30.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976s/03may11.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976s/03may17.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/c115.2976s/03may19.raw/n2976.lc.usb',
                '../../sting-co/sdi/bima/n2976/d115.2976s/03jul01.raw/n2976.lc.usb',
                '../../sting-co/sdi/n2976/vis/ngc2976_C1_10SEP30.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C2_10OCT02.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C3_10OCT12.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C4_10OCT13.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C5_10OCT13.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C6_10OCT14.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C7_10OCT29.co.cal',
                '../../sting-co/sdi/n2976/vis/ngc2976_C8_10NOV01.co.cal']

for i in range(0,len(mirfile_list)):
    execfile(xlib+'xinit.py')
    xp['rawfiles']=mirfile_list[i]
    xp['prefix']=track_list[i]+'.src'
    xp['importmode']='mir'
    xp['importmirarray']=telescopes[i]
    #execfile(xlib+'ximport.py')
     
# CONSOLIDATING 

xp['prefix_comb']       =track_list
xp['prefix']            ='n2976co'
xp['usevconcat']        =False # visstate doesn't work well withMS from virtualconcat

# IMAGING
xp['cleanmode']         ='velocity'
xp['clean_start']       ='-100km/s'
xp['clean_nchan']       =(200)/5+1
xp['clean_width']       ='5km/s'
xp['restfreq']          ='115.2712GHz'
xp['outframe']          ='LSRK'

xp['phasecenter']       ='J2000 09h47m15.40 67d54m59.00'
xp['imsize']            =350
xp['cell']              ='1arcsec'

xp['multiscale']        =[0,3,9]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0
xp['minpb']             =0.20
xp['clean_mask']        =0.25

#execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')