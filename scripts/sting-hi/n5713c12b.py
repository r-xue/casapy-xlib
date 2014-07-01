execfile(xlib+'xinit.py')

# IMPORT
xp['prefix']            =os.path.splitext(os.path.basename(os.path.realpath(inspect.stack()[0][1])))[0]
xp['rawfiles']          ='/Volumes/Scratch/raw/21cm/n5713/12A-270.sb8048385.eb8591108.55979.37765980324.ms'
xp['importmode']        ='ms'
xp['importspw']         ='2,3,4,10,11,12'
xp['importchanbin']     =4
xp['importtimebin']     ='30s'

# CALIBRATION
xp['source']            ='NGC 5713'
xp['spw_source']        ='0,1,2,3,4,5'

xp['fluxcal']           ='3C286'
xp['uvrange_fluxcal']   =''
xp['phasecal']          ='J1445+0958'
xp['uvrange_phasecal']  =''

# rfi at the spw center
xp['flagselect']        =[  "antenna='ea06&ea22'",
                            "antenna='ea06&ea19'",
                            "antenna='ea06&ea17'",
                            "timerange='10:08:20~10:11:40' field='NGC 5713'",
                            "timerange='10:18:20~10:20:50' field='NGC 5713'",
                            "timerange='10:27:30~10:30:00' field='NGC 5713'",
                            "timerange='10:55:00~10:56:40' field='NGC 5713'"]
xp['flagtsys_range']    =[5.0,200.0]

execfile(stinghi+'n5713_config.py')
xp['niter']             =0

# RUN SCRIPTS:
#execfile(xlib+'ximport.py')
#xu.checkvrange(xp['prefix']+'.ms')
#au.timeOnSource(xp['prefix']+'.ms')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')
