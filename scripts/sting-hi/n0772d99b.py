execfile(xlib+'xinit.py')

# IMPORT
xp['prefix']            =os.path.splitext(os.path.basename(os.path.realpath(inspect.stack()[0][1])))[0] 
xp['rawfiles']          =['/Volumes/Scratch/raw/21cm/n0772/AG564_4',
                          '/Volumes/Scratch/raw/21cm/n0772/AG564_5']
xp['importspw']         ='1'

# CALIBRATION
xp['source']            ='ARP78'
xp['spw_source']        ='0'

xp['fluxcal']           = '0137+331'
xp['uvrange_fluxcal']   ='<40klambda'
xp['phasecal']          = '0204+152'
xp['uvrange_phasecal']  ='<100klambda'

xp['flagspw']           ='0:0~4;122~126'
xp['flagselect']        = [ #"timerange='16:06:40~17:29:15'", 
                            "timerange='19:57:25~19:57:35'", 
                            "timerange='17:38:00~17:40:00'",
                            "field='0137+331' uvrange='<800lambda'",
                            "field='0204+152' uvrange='<800lambda'",
                            "timerange='19:51:20~19:54:00' antenna='VA05'",
                            "antenna='VA14&VA24'",
                            "antenna='VA14&VA28'",
                            "antenna='VA14&VA12'",
                            "antenna='VA19&VA26'"]
xp['flagselect']        = [ "timerange='16:06:40~17:29:15' field='ARP78' uvrange='<800lambda'", 
                            "timerange='19:57:25~19:57:35'", 
                            "timerange='17:38:00~17:40:00'",
                            "field='0137+331' uvrange='<800lambda'",
                            "field='0204+152' uvrange='<800lambda'",
                            "timerange='19:51:20~19:54:00' antenna='VA05'",
                            ]

execfile(stinghi+'n0772_config.py')
xp['niter']             =0

# RUN SCRIPTS:
#execfile(xlib+'ximport.py')
#xu.checkvrange(xp['prefix']+'.ms')
#au.timeOnSource(xp['prefix']+'.ms')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')
