execfile(xlib+'xinit.py')

# IMPORT
xp['prefix']        =os.path.splitext(os.path.basename(os.path.realpath(inspect.stack()[0][1])))[0]
xp['rawfiles']      ='../../../raw/21cm/n0337/AT285_1'
xp['importspw']     ='0,1'
xp['importscan']    ='2~5'

# CALIBRATION
xp['source']            ='NGC0337'
xp['spw_source']        ='0,1'

xp['fluxcal']           ='0137+331'
xp['uvrange_fluxcal']   ='<40klambda'
xp['phasecal']          ='0059+001'


xp['flagspw']           ="0:0~4;60~62,1:0~2;58~62"
xp['flagselect']        =[  "timerange='2003/02/16/22:06:02~22:06:30' field='0137+331'",
                            "antenna='VA08&VA11'",
                            "antenna='VA20&VA11'",
                            "antenna='VA03&VA08'",
                            "antenna='VA03&VA09'",
                            "antenna='VA03&VA10'",
                            "antenna='VA14&VA27'",
                            "antenna='VA08&VA14'",
                            "antenna='VA08&VA10'",
                            "antenna='VA04&VA20'",
                            "antenna='VA10&VA15'",
                            "antenna='VA09&VA19'",
                            "antenna='VA02&VA03'"]

# CONSOLIDATING
xp['spwrgd']            ='spw'
xp['scalewt']           =True
xp['imcs']              =True
xp['fitchans']          ='0~22;84~106'
xp['fitorder']          =1

# IMAGING
xp['cleanspec']         =True

xp['imsize']            =320
xp['cell']              ='8.0arcsec'

xp['imstat_box_spec']   ='42,103,117,175'

xp['cleanmode']         ='velocity'
xp['clean_start']       ='1360.00km/s'
xp['clean_width']       ='5.2km/s'
xp['clean_nchan']       =107
xp['phasecenter']       ='J2000 00h59m50.1 -07d34m41.0'
xp['niter']             =0
xp['usescratch']        =True

# RUN SCRIPTS:
execfile(xlib+'ximport.py')
execfile(xlib+'xcal.py')
execfile(xlib+'xconsol.py')
execfile(xlib+'xclean.py')

