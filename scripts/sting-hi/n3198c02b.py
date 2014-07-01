execfile(xlib+'xinit.py')

xp['prefix']        =os.path.splitext(os.path.basename(os.path.realpath(inspect.stack()[0][1])))[0]
xp['rawfiles']      =['../n3198/AT285_5']
xp['starttime']     ='2002/11/19/11:23:30'
xp['stoptime']      ='2002/11/19/12:47:50'


# TRACK INFORMATION
xp['source']        ='NGC3198'
xp['spw_source']    ='0,1'

xp['fluxcal']             = '1331+305'
xp['fluxcal_uvrange']    =''
xp['phasecal']             = '1006+349'
xp['phasecal_uvrange']    ='<30klambda'


# CALIBRATION & OPTIONS
xp['flagspw']       ='*:0;60~62'
xp['flagselect'] = [
                "mode='quack' quackinterval=20.0 field='1006+349'",
                "antenna='VA09&VA14'"
                    ]


execfile(stinghi+'n3198_config.py')
xp['niter']        =0

# RUN SCRIPTS
#execfile(xlib+'ximport.py')
#xu.checkvrange(xp['prefix']+'.ms')
#au.timeOnSource(xp['prefix']+'.ms')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')




