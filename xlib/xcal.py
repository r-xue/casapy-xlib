#########################################################################################
#

#   PURPOSE
#
#       Inspect, flag, and calibrate data
#
#   INPUT FILE
#       Mesaurement Set:    <prefix>.ms
#
#   OUTPUT FILE
#       Measurement Set:    <prefix>.ms 
#                           -- calibrated data in the "corrected" column
#       Calibration Table:  <prefix>.bcal 
#                           -- passband solution table
#                           <prefix>.gcal
#                           -- gain solution table
#                           <prefix>.fcal
#                           -- flux-corrected gain solution table
#
#   INPUT KEYWORD [ OPTIONAL | DEFAULT VALUE]
#
#       prefix|'test'           name of the measurment Set
#
#       source|''               source name
#       phasecal|''             phase calibrator name
#       phasecal_uvrange|''     uvrange selection for the phase calibrator
#                               (check the VLA CALIBRATOR MANUAL)
#       fluxcal|''              flux calibrator name
#       fluxcal_uvrange|''      uvrange selection for the flux calibrator
#                               (check the VLA CALIBRATOR MANUAL)       
#       passcal|<fluxcal>       passband calibrator name
#                               the default value is the flux calibrator
#       passcal_uvrange|<fluxcal_uvrange>   
#                               uvrange selection for the passband calibrator
#       
#       spw_source|''                  spectral windows for source
#       spw_fluxcal|<spw_source>       spectral Windows for fluxcal     
#       spw_phasecal|<spw_source>      spectral Windows for phasecal
#       spw_passcal|<spw_fluxcakl>     spectral Windows for passcal

#       ref_ant|'15'            reference antenna name. 
#       gaincurve               gain-elevation curve calibration
#                               default=TRUE if the data were taken from VLA/EVLA 
#                               after 2001
#
#       flagreset|True          reset flagging, if False, the previous flagging info
#                               saved in 'flagged' will be reused
#
#       flagselect|''           string list for selecting the data to be flagged.
#       flagtest|False          True: the script will stop after flagging
#       calwt|True              set False for data taken without reliable weighting info
#
#       bcant|''                antennas for baseline correction
#       bctype|'antposvla'      baseline correction type
#       bcpara|[]               baseline correction parameter
#
#       Example for Baseline Corrections:
#           bcant='VA06,VA02,VA03,VA07,VA10,VA11,VA16,VA17,VA18,VA19'
#           bcpara=[    -0.0063, -0.0205,  0.0102,
#                        0.0000,  0.0003, -0.0007,
#                       -0.0011,  0.0003, -0.0005,
#                       -0.0013,  0.0000,  0.0000,
#                       -0.0013,  0.0004,  0.0000,
#                       -0.0007,  0.0000,  0.0000,
#                        0.0000, -0.0006,  0.0000,
#                       -0.0008,  0.0000,  0.0000,
#                        0.0000, -0.0004,  0.0000,
#                        0.0000, -0.0004,  0.0000]
#
#   HISTORY
#
#       20090324    RX  deriving refspw_map
#       20110617    RX  add calwt for data without valid weights
#       20110916    RX  minor fixes for v3.3 / dual-pol tracks
#       20111006    RX  fix a bug for dual-pol tracks
#       20130214    RX  use <gencal> for gaincurve/baseline calibrations
#                       bandpass transfer implemented
#       20130910    RX  use global dict variable <xp> to wrap pipeline parameters
#
#   AUTHOR
#
#       Rui Xue, University of Illinois
#
#########################################################################################

#----------------------------------------------------------------------------------------
#   Environment Setup
#----------------------------------------------------------------------------------------
casalog.filter('INFO')

startTime=time.time()
xu.news("")
xu.news("++")
xu.news("------------- Begin Task: XCAL "+xp['prefix']+" -------------")
xu.news("++")
xu.news("")
casa_log = open(casalog.logfile(),'r')
startlog = casa_log.readlines()
casa_log.close()

xp['msfile'] = xp['prefix'] + '.ms'
#os.system('rm -rf '+xp['prefix']+'.psf'+'*')
#os.system('rm -rf '+xp['prefix']+'.flux'+'*')
#os.system('rm -rf '+xp['prefix']+'.residual'+'*')
#os.system('rm -rf '+xp['prefix']+'.model'+'*')
os.system('rm -rf '+xp['prefix']+'.?cal'+'*')

xu.news("")
xu.news(">>>>check for flagversion Original")
xu.news("")
if    os.path.exists(xp['prefix']+'.ms.flagversions/flags.Original'):
    xu.news("flagversion 'Original' exists ")
    xu.news("")
else:
    xu.news("flagversion 'Original' doesn't exist")
    xu.news("")
    xu.news("save it for flagversion backup")
    xu.news("")
    flagmanager(vis = xp['msfile'],
                mode='save',
                versionname='Original',
                comment='Original Flagging',
                merge='replace')


if  xp['passcal']=='':
    xp['passcal']=xp['fluxcal']
    xp['uvrange_passcal']=xp['uvrange_fluxcal']

if  xp['spw_phasecal']=='':
    xp['spw_phasecal']=xp['spw_source']

if  xp['spw_fluxcal']=='':
    xp['spw_fluxcal']=xp['spw_source']

if  xp['spw_passcal']=='':
    xp['spw_passcal']=xp['spw_fluxcal']


spwid_source=xp['spw_source'].split(',')
spwid_passcal=xp['spw_passcal'].split(',')
spwid_phasecal=xp['spw_phasecal'].split(',')
spwid_fluxcal=xp['spw_fluxcal'].split(',')
spwid_soucal=spwid_source+spwid_passcal+spwid_fluxcal+spwid_phasecal
spwid_soucal=sorted(list(set(spwid_soucal)))


tb.open(xp['msfile']+"/OBSERVATION",nomodify=True)
namelist=tb.getcol("TELESCOPE_NAME").tolist()
obstime=tb.getcol("TIME_RANGE").tolist()
tb.close()
isvla=False
isafter2001=False
utc2001=86400*(me.epoch('utc','2003/02/16')['m0']['value']+0./24.)
for k in range(len(namelist)):
    if  namelist[k]=='VLA' or namelist[k]=='EVLA' :
        isvla=True
    if  obstime[k][0]>utc2001:
        isafter2001=True
if  isvla==True and isafter2001==True:
    xp['gaincurve']=True
xu.news("gaincurve calibration?: "+str(xp['gaincurve']))
xu.news("")

xp['gaincurve']=False
#----------------------------------------------------------------------------------------
#   Flagging Resetting (default: True)
#----------------------------------------------------------------------------------------

if  xp['flagreset']==True:
    flagmanager(vis=xp['prefix']+'.ms',mode='restore',versionname='Original')
if  xp['flagreset']==False:
    flagmanager(vis=xp['prefix']+'.ms',mode='restore',versionname='flagged')

#----------------------------------------------------------------------------------------
#   Edge / Shadow / Autocorr / Quack Flagging
#----------------------------------------------------------------------------------------



xu.news("")
xu.news("--flagcmd--")
xu.news("")
xu.news("Shadow Flagging")
xu.news("Auto-correlation Flagging")    
xu.news("")
xu.news("Edge channels Flagging")
xu.news(">>>spw_flagged: "+xp['flagspw'])
xu.news("")
if  xp['flagselect']!='':
    xu.news("Manual Selection Flagging")
    xu.news(">>>flagselect: ")
    for i in range(0,len(xp['flagselect'])):
        xu.news("   "+(xp['flagselect'])[i])
    xu.news("")

if  type(xp['flagselect'])==type(''):
    xp['flagselect']=[xp['flagselect']]
if  xp['flagspw']!='':
    xp['flagselect']=xp['flagselect']+["spw='"+xp['flagspw']+"'"]
xp['flagselect']=xp['flagselect']+["antenna='*&&&'","mode='shadow'"]
os.system('rm -rf '+xp['msfile']+'.flagcmd.log')

flagcmd(vis=xp['msfile'],
        inpmode='list',
        inpfile=xp['flagselect'],
        savepars=True,
        outfile=xp['msfile']+'.flagcmd.log',        
        flagbackup=False)

if  xp['flagtest']==True:
    xu.news("---------------------")
    xu.news("FlagTest Mode is used")
    xu.news("---------------------")
    xu.news("The script stopped after flagging based on the flagselect keyword")
    xu.news("Waiting for your inspection using plotms (recommended) or plotxy")
    xp['flagtest']=False
    xp['flagselect']=[]
    flagmanager(vis=xp['prefix']+'.ms',
                mode='save',versionname='flagtest',merge='replace')    
    sys.exit("Please ignore the above color Trackback error message")

#----------------------------------------------------------------------------------------
#   Save flagging information
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--flagmanager--")
xu.news("")
xu.news("save the flagging we just did")
xu.news("")

flagmanager(vis = xp['msfile'],
            mode='save',
            versionname='FlagCMD',
            comment='Flagging After FLAGCMD',
            merge='replace')

xu.news("")
xu.news("list the current flag versions")
xu.news("")
flagmanager(vis = xp['msfile'],
            mode='list',
            versionname='FlagCMD',
            comment='Flagging After FLAGCMD',
            merge='replace')
xu.news("")


#----------------------------------------------------------------------------------------
#   CALIBRATION BEGIN
#   EVLA GAIN
#----------------------------------------------------------------------------------------

if  xp['evlacal']==True:

    xu.news("")
    xu.news("--gencal--")
    xu.news("")
    xu.news("Get EVLA gain/tsys calibration table using info from")
    xu.news("the MS's CALDEVICE and SYSPOWER subtables.")
    xu.news("")
    gencal(vis=xp['msfile'],
           caltype='evlagain',
           caltable=xp['prefix']+'.tcal')

#----------------------------------------------------------------------------------------
#   Baseline Correction
#----------------------------------------------------------------------------------------

if  xp['bcant']!='':

    xu.news("")
    xu.news("--gencal--")
    xu.news("")
    xu.news("solve baseline correction solutions")
    xu.news("")
    gencal(vis=xp['msfile'],
           caltable=xp['prefix']+'.pcal',
           caltype=xp['bctype'],
           antenna=xp['bcant'],
           parameter=xp['bcpara'])


#----------------------------------------------------------------------------------------
#   Gaincurve Correction
#----------------------------------------------------------------------------------------

if  xp['gaincurve']==True:

    xu.news("")
    xu.news("--gencal--")
    xu.news("")
    xu.news("solve gaincurve correction solutions")
    xu.news("")
    gencal(vis=xp['msfile'],
           caltable=xp['prefix']+'.gccal',
           caltype='gceff')

#----------------------------------------------------------------------------------------
#   CALIBRATION BEGIN
#   Fill the model column with the model visibilities of the flux calibrator
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--setjy--")
xu.news("")
xu.news("find the model flux density of flux calibrators, Fourier transfter the model to") 
xu.news("visibilities and write them into the MODEL_DATA column of the current MS")
xu.news("")

setjy(vis=xp['msfile'],
      field=xp['fluxcal'],
      spw=xp['spw_fluxcal'],
      scalebychan=True)
xu.news("")

#----------------------------------------------------------------------------------------
#   Calculate Bandpass Solutions
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--gaincal--")
xu.news("")
xu.news("calculate passcal gain to improve bandpass solutions")
xu.news("")

gaintable=[]
gainfield=[]
if  xp['evlacal']==True:
    gaintable=gaintable+[xp['prefix']+'.tcal']
    gainfield=gainfield+['']
if  xp['bcant']!='':
    gaintable=gaintable+[xp['prefix']+'.pcal']
    gainfield=gainfield+['']
if  xp['gaincurve']==True:
    gaintable=gaintable+[xp['prefix']+'.gccal']
    gainfield=gainfield+['']   
            
gaincal(vis=xp['msfile'],
        caltable=xp['prefix']+'.gcal_passcal',
        field=xp['passcal'],
        spw=xp['spw_passcal'],
        uvrange=xp['uvrange_passcal'],        
        solint='inf',
        combine='',
        refant=xp['ref_ant'],
        minsnr=3.0,
        solnorm=False,
        gaintable=gaintable,
        gainfield=gainfield)

xu.news("")
xu.news("")
xu.news("--bandpass--")
xu.news("")
xu.news("calculate bandpass solutions for each spw in spw_passcal")
xu.news("")
xu.news("")

gaintable=gaintable+[xp['prefix']+'.gcal_passcal']
gainfield=gainfield+['']   
    
bandpass(vis=xp['msfile'],
         caltable=xp['prefix']+'.bcal',
         field=xp['passcal'],
         spw=xp['spw_passcal'],
         uvrange=xp['uvrange_passcal'],
         solint='inf',
         solnorm=True,
         refant=xp['ref_ant'],
         selectdata=False,
         bandtype='B',
         combine='scan',
         gaintable=gaintable,
         gainfield=gainfield)
xu.news("")

# SPECIAL TREATMENT FOR SOME HI TRACKS
if  len(spwid_passcal)==2*len(spwid_source):
    
    xu.news("")
    xu.news("--bandpass--")
    xu.news("")
    xu.news("calculate spw-combined bandpass solutions")
    xu.news("")
    xu.news("")
       
    for i in range(0,len(spwid_source)):
        
        spw_solvebandpass=str(spwid_passcal[i])+','\
            +str(spwid_passcal[i+len(spwid_source)])
        xu.news("")
        xu.news('->')
        xu.news("processing bandpass spw: "+spw_solvebandpass)
        xu.news('for source spw: '+str(spwid_source[i]))
        xu.news('save bandpass solution to spw: '+str(spwid_passcal[i]))
        xu.news('->')
        xu.news("")
        bandpass(vis=xp['msfile'],
                 caltable=xp['prefix']+'.bcal_comb',
                 field=xp['passcal'],
                 spw=spw_solvebandpass,
                 solint='inf',
                 solnorm=True,
                 refant=xp['ref_ant'],
                 selectdata=False,
                 gaincurve=False,
                 bandtype='B',
                 uvrange=xp['uvrange_passcal'],
                 combine='spw,scan',
                 gaintable=gaintable,
                 gainfield=gainfield,
                 append=True)
        xu.news("")

#----------------------------------------------------------------------------------------
#   Calculate Gain Solutions
#----------------------------------------------------------------------------------------


tb.open(xp['msfile']+'/SPECTRAL_WINDOW',nomodify=False)
header_para=tb.colnames()
if 'DOPPLER_ID' in header_para:
    spwid=tb.getcol('DOPPLER_ID')
else:  
    spwid='0'
num_chan = tb.getcol('NUM_CHAN')
ref_freq = tb.getcol('REF_FREQUENCY')
tb.close()

tb.open(xp['msfile']+'/DATA_DESCRIPTION',nomodify=False)
header_para=tb.colnames()
if 'SPECTRAL_WINDOW_ID' in header_para:
    spwid=tb.getcol('SPECTRAL_WINDOW_ID')
else:
    spwid='0'
tb.close()

spwid=list(spwid)
for i in range(0,len(spwid)):
    spwid[i]=int(spwid[i])

xu.news("")
xu.news("--gaincal--")
xu.news("")
xu.news("Calculate the Gain Solutions for Phase/Flux calibrators")
xu.news("")

xu.news("")
xu.news("-orginal gaincal spwmap: ")
xu.news(spwid)
xu.news("")

spwmap_phasecal=list(spwid)
for i in range(0,len(spwid_phasecal)):
    if  i<len(spwid_passcal):
        spwmap_phasecal[int(spwid_phasecal[i])]=int(spwid_passcal[i])
    else:
        spwmap_phasecal[int(spwid_phasecal[i])]=int(spwid_passcal[i-len(spwid_passcal)])

spwmap_fluxcal=list(spwid)
for i in range(0,len(spwid_fluxcal)):
    if  i<len(spwid_passcal):
        spwmap_fluxcal[int(spwid_fluxcal[i])]=int(spwid_passcal[i])
    else:
        spwmap_fluxcal[int(spwid_fluxcal[i])]=int(spwid_passcal[i-len(spwid_passcal)])

xu.news('')
xu.news('->')
xu.news('spwmap_bcal->phasecal:'+str(spwmap_phasecal))
xu.news('spwmap_bcal->fluxcal:'+str(spwmap_fluxcal))
xu.news('->')
xu.news('')


gainfield[-1]=xp['passcal']
if  2*len(spwid_fluxcal)==len(spwid_passcal):
    gaintable[-1]=xp['prefix'] + '.bcal_comb'
else:
    gaintable[-1]=xp['prefix'] + '.bcal'
spwmap=[[]]*len(gaintable)
interp=['nearest']*len(gaintable)

for j in range(0,len(spwid_source)):
    
    spw_solvegain_fluxcal=str(spwid_fluxcal[j])
    if  len(spwid_fluxcal)==2*len(spwid_source):
        spw_solvegain_fluxcal=spw_solvegain_fluxcal+','+str(spwid_fluxcal[j+len(spwid_source)])
    spw_solvegain_phasecal=str(spwid_phasecal[j])
    if  len(spwid_phasecal)==2*len(spwid_source):
        spw_solvegain_phasecal=spw_solvegain_phasecal+','+str(spwid_phasecal[j+len(spwid_source)])
    
    spwmap[-1]=spwmap_fluxcal
    gaincal(vis=xp['msfile'],
            field=xp['fluxcal'],
            uvrange=xp['uvrange_fluxcal'],
            spw= spw_solvegain_fluxcal,
            caltable=xp['prefix']+'.gcal',
            spwmap=spwmap,
            selectdata=True,
            solint='inf',
            minsnr=3.0,
            minblperant=2,
            refant=xp['ref_ant'],
            combine='spw',
            append= True)

    spwmap[-1]=spwmap_phasecal
    gaincal(vis=xp['msfile'],
            field=xp['phasecal'],
            uvrange=xp['uvrange_phasecal'],
            spw=spw_solvegain_phasecal,
            caltable=xp['prefix']+'.gcal',
            spwmap=spwmap,
            selectdata=True,
            solint='inf',
            minsnr=3.0,
            minblperant=2,
            refant=xp['ref_ant'],
            combine='spw',
            append= True)    

    xu.news("")

#----------------------------------------------------------------------------------------
#   Bootstrap flux of the phasecal source
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--fluxscale--")
xu.news("")
xu.news("calculate flux scaling and get a flux-scaled gain table")
xu.news("see Log window for flux value found")

refspw_map=list(spwid)
xu.news("")
xu.news("-orginal fluxscale refspwmap: ")
xu.news(refspw_map)
xu.news("")

for i in range(0, len(spwid_phasecal)):
    if  i<len(spwid_fluxcal):
        refspw_map[int(spwid_phasecal[i])]=int(spwid_fluxcal[i])
    else:
        refspw_map[int(spwid_phasecal[i])]=int(spwid_fluxcal[i-len(spwid_fluxcal)])


xu.news("")
xu.news("-modified fluxscale refspwmap: ")
xu.news(refspw_map)
xu.news("")

if  xp['phasecal']!=xp['fluxcal']: 
    fluxscale(vis=xp['msfile'],
              caltable=xp['prefix']+'.gcal',
              transfer=xp['phasecal'],
              fluxtable=xp['prefix']+'.fcal',
              reference=xp['fluxcal'],
              refspwmap=refspw_map)
else: 
    os.system("cp -rf "+xp['prefix']+".gcal "+xp['prefix']+".fcal")
xu.news("")

#----------------------------------------------------------------------------------------
#   Apply Calibration Tables - Results go to the corrected_data column 
#   Using Bandpass and Gain Solutions
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--applycal--")
xu.news("")
xu.news("apply calibration tables (flux-scaled gain + bandpass) and ")
xu.news("writes calibrated data to the CORRECTED_DATA column..")


spwmap_bcal2source=list(spwid)
spwmap_fcal2source=list(spwid)
for i in range(0, len(spwid_source)):
    spwmap_bcal2source[int(spwid_source[i])]=int(spwid_passcal[i])
    spwmap_fcal2source[int(spwid_source[i])]=int(spwid_phasecal[i])

spwmap_bcal2phasecal=list(spwid)
spwmap_fcal2phasecal=list(spwid)
for i in range(0, len(spwid_phasecal)):    
    if  i<len(spwid_passcal):
        spwmap_bcal2phasecal[int(spwid_phasecal[i])]=int(spwid_passcal[i])
    else:
        spwmap_bcal2phasecal[int(spwid_phasecal[i])]=int(spwid_passcal[i-len(spwid_passcal)])
    if  i<len(spwid_source):
        spwmap_fcal2phasecal[int(spwid_phasecal[i])]=int(spwid_phasecal[i])
    else:
        spwmap_fcal2phasecal[int(spwid_phasecal[i])]=int(spwid_phasecal[i-len(spwid_source)])

spwmap_bcal2fluxcal=list(spwid)
spwmap_fcal2fluxcal=list(spwid)
for i in range(0, len(spwid_fluxcal)):    
    if  i<len(spwid_passcal):
        spwmap_bcal2fluxcal[int(spwid_fluxcal[i])]=int(spwid_passcal[i])
    else:
        spwmap_bcal2fluxcal[int(spwid_fluxcal[i])]=int(spwid_passcal[i-len(spwid_passcal)])
    if  i<len(spwid_source):
        spwmap_fcal2fluxcal[int(spwid_fluxcal[i])]=int(spwid_fluxcal[i])
    else:
        spwmap_fcal2fluxcal[int(spwid_fluxcal[i])]=int(spwid_fluxcal[i-len(spwid_source)])


gaintable=gaintable+[xp['prefix']+'.fcal']
gainfield=gainfield+[xp['phasecal']]

spwmap=spwmap+[spwmap_fcal2source]
spwmap[-2]=spwmap_bcal2source
interp=interp+['linear']
applycal(vis=xp['msfile'],
         field=xp['source'],
         spw=xp['spw_source'],
         calwt =xp['calwt'],
         flagbackup=False,
         gaintable=gaintable,
         interp=interp,
         gainfield=gainfield,
         spwmap=spwmap)

xu.news('')
xu.news('->')
xu.news('spwmap_fcal->source:'+str(spwmap_fcal2source))
xu.news('spwmap_bcal->source:'+str(spwmap_bcal2source))
xu.news('->')
xu.news('')

spwmap[-2]=spwmap_bcal2phasecal
spwmap[-1]=spwmap_fcal2phasecal
interp[-1]='nearest'
applycal(vis=xp['msfile'],
         field=xp['phasecal'],
         spw=xp['spw_phasecal'],
         calwt =xp['calwt'],
         flagbackup=False,
         gaintable=gaintable,
         interp=interp,
         gainfield=gainfield,
         spwmap=spwmap)

xu.news('')
xu.news('->')
xu.news('spwmap_fcal->phasecal:'+str(spwmap_fcal2phasecal))
xu.news('spwmap_bcal->phasecal:'+str(spwmap_bcal2phasecal))
xu.news('->')
xu.news('')

spwmap[-2]=spwmap_bcal2fluxcal
spwmap[-1]=spwmap_fcal2fluxcal
gainfield[-1]=xp['fluxcal']
applycal(vis=xp['msfile'],
         field=xp['fluxcal'],
         spw=xp['spw_fluxcal'],
         calwt =xp['calwt'],
         flagbackup=False,
         gaintable=gaintable,
         interp=interp,
         gainfield=gainfield,
         spwmap=spwmap)

xu.news('')
xu.news('->')
xu.news('spwmap_fcal->fluxcal:'+str(spwmap_fcal2fluxcal))
xu.news('spwmap_bcal->fluxcal:'+str(spwmap_bcal2fluxcal))
xu.news('->')
xu.news('')

#----------------------------------------------------------------------------------------
#   Save flagging information
#----------------------------------------------------------------------------------------
xu.news("")
xu.news("--flagmanager--")
xu.news("")
xu.news("save the flagging after applying calibration tables")
xu.news("")

flagmanager(vis=xp['msfile'],
            mode='save',
            versionname='ApplyCal',
            comment='Flagging After ApplyCAL',
            merge='replace')

xu.news("")
xu.news("list the current flag versions")
xu.news("")
flagmanager(vis=xp['msfile'],
            mode='list',
            versionname='ApplyCal',
            comment='Flagging After ApplyCAL',
            merge='replace')
xu.news("")

#----------------------------------------------------------------------------------------
#   End Statement
#----------------------------------------------------------------------------------------

flagcal2time=time.time()
xu.news("")
xu.news("Total flagging and calibration time: %10.1f" %(flagcal2time-startTime))
xu.news("")
xu.news("++")
xu.news("------------- End Task: XCAL "+xp['prefix']+" -------------")
xu.news("++")
xu.news("")
casa_log = open(casalog.logfile(),'r')
stoplog = casa_log.readlines()
casa_log.close()
xu.exportcasalog(startlog,stoplog, xp['prefix']+'.xcal.reduc.log')

if  xp['email']!='':
    emailsender(xp['email'],\
                "RUN XCAL End: "+xp['prefix'],\
                "This email was generated automatically by your successful \
                reduction run.\nThe log files are attached",\
                [xp['prefix']+'.xcal.reduc.log'])
                