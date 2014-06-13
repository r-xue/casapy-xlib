execfile(xlib+'xinit.py')

xp['prefix']        ='n3198d03b'
xp['rawfiles']      =[rawdir+'/n3198/AT285_12']
xp['starttime']     ='2003/04/28/04:10:50.0'
xp['stoptime']      ='2003/04/28/04:36:50.0'

# TRACK INFORMATION
xp['source']        ='NGC3198'
xp['spw_source']    ='0,1'

xp['fluxcal']             = '1331+305'
xp['fluxcal_uvrange']    =''
xp['phasecal']             = '1006+349'
xp['phasecal_uvrange']    ='<30klambda'
spw_edge =6

# CALIBRATION & OPTIONS
xp['flagselect'] = [    "timerange='2003/04/28/04:18:20~04:19:25' field='1331+305'"
                ]

execfile(stinghi+'n3198_config.py')
xp['niter']        =0

# RUN SCRIPTS
execfile(xlib+'ximport.py')
xu.checkvrange(xp['prefix']+'.ms')
au.timeOnSource(xp['prefix']+'.ms')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')


