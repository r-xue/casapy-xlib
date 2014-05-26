execfile(xlib+'xinit.py')

# IMPORT
xp['prefix']            ='n4254d'
xp['rawfiles']          =['/Volumes/Scratch/raw/21cm/n4254/AP206_1']
xp['importspw']         ='0'

# CALIBRATION
xp['source']            ='NGC4254'
xp['fluxcal']           ='1331+305'
xp['fluxcal_uvrange']   =''
xp['phasecal']          ='1221+282'
xp['phasecal_uvrange']  =''
xp['spw_source']        ='0'

xp['flagselect']        =["timerange='10:29:30~10:30:00'"]

# CONSOLIDATING & IMAGING
execfile(stinghi+'n4254/n4254_config.py')
xp['niter']             =0

# RUN SCRIPTS:
execfile(xlib+'ximport.py')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')