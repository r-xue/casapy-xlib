#1474->1792
execfile(stinghi+'n0337c06.py')
execfile(stinghi+'n0337d03.py')

execfile(xlib+'xinit.py')

# CONSOLIDATING
xp['prefix']            =os.path.splitext(os.path.basename(os.path.realpath(inspect.stack()[0][1])))[0]
xp['prefix_comb']       =['n0337d03','n0337c06']


xp['imcs']              =True
xp['fitchans']          ='0~13;77~94'
xp['fitorder']          =1

# IMAGING
xp['cleanspec']         =True

xp['imsize']            =2**5*10
xp['cell']              ='8.0arcsec'

xp['imstat_box_spec']   ='34,153,120,278'

xp['cleanmode']         ='velocity'
xp['clean_start']       ='1401.6km/s'
xp['clean_width']       ='5.2km/s'
xp['clean_nchan']       =95
xp['phase_center']      ='J2000 00h59m50.1 -07d34m41.0'

xp['multiscale']        =[0,3,9]
xp['clean_gain']        =0.3
xp['cyclefactor']       =5.0
xp['negcomponent']      =0

# RUN SCRIPTS:
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')

