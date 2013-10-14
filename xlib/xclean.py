#########################################################################################
#
#   PURPOSE
#       
#       imaging the calibrated data
#
#   INPUT FILE
#       
#       Mesaurement Set:    <prefix>.src.ms
#                           <prefix>.src.ms.contsub 
#
#
#   INPUT KEYWORD [ OPTIONAL | DEFAULT VALUE ]

#       prefix|'test'       Name of the Measurment Set
#
#       imcs|False          True: the script will perform IMCONTSUB. 
#       fitchans|''         image cube channel selection for fitting the continuum in 
#                           IMCONTSUB (e.g., fitchans='1~7;79~85')    
#       fitorder|0          polynomial order for fitting the continuum in IMCONTSUB
#
#       imsize|512          imaging size (numbers of pixels)
#       cell|'4.0arcsec'    imaging pixel size.

#       clean_mask|0.2      some other examples (see help->clean):
#                           [0,0,511,511]        use a box
#                           TrueL                use the minpb value
#                           'cleanbox.txt'       use a cleanbox file 
#
#       imstat_box_spec     Box for the <sig> calculation default: inner quarters
#       imstat_box_cont     Box for the <sig> calculation default: four corners
#
#       imstat_chan|''      channels for the <sig> calculation
#
#       imstat_rg_spec|''   region for the <sig> calculation
#       imatst_rg_cont|''   region for the <sig> calculation
#
#       sigcutoff_spec|2.0  <sigcutoff_spec>*<sig> is the default threshold value for
#                           spectral-cube CLEAN 
#                           <sig> is calculated from the dirty cube using line-free 
#                           channels&region.
#       sigcutoff_cont|2.0  <sigcutoff_cont>*<sig> is the default threshold value for
#                           continuum-image MSF CLEAN 
#                           <sig> is calculated from the dirty image using line-free 
#                           region
#
#       threshold_spec|<sigcutoff_spec>*<sig>/ units-mJy:  
#                           threshold for spec cleaning
#       threshold_cont|<sigcutoff_cont>*<sig>/ units-mJy:  
#                           threshold for mfs cleaning
#       n_iter|10000        iteration threshold for clean
#
#       cleanmode:          "channel" or "velocity"
#       clean_start:        First channel/velocity to clean
#       clean_nchan:        Number of planes in the output image
#       clean_width:        Number of input channels to average 
#                           or the velocity width for each image plane
#       restfreq|'1420405752.0Hz'    
#                           rest frequency for imaging
#       outframe|'BARY'     frame of the output image
#       spinterpmode|'linear' 
#                           spectral gridding interpolation mode in CLEAN                         
#
#       phasecenter|''      phasecenter for clean 
#                           e.g. 'J2000 12h18m49.6 14d24m59.01' or '2' (=fieldid2)

#       imagermode          imagermode for clean, options include: 'csclean', 'mosaic' 
#                           'mosaic' must be be used if your science target is in 
#                           multiple fields or it's heterogeneous-array observation.
#                           'csclean' for single point+homogeneous array data. 
#       ftmachine|'ft'      ftmachine='mosaic' may be buggy for track combination 
#                           right now. For CARMA, you must always use 
#                           ftmachine='mosaic', because it is a heterogeneous array.
#       weight|'briggs'     other options: 'briggs', 'uniform' or 'natural'
#       wrobust|0.5         robust weight R parameter
#
#       outertaper|[]       taper function for weighting
#       multiscale|[]       using multi-scale clean is not the default setting
#                           multi_scale=[0,1,3,10,30] is recommened, and units is pixel
#       clean_gain|0.1      gain factor for clean, 
#                           for multiscale clean, clean_gain=0.7 is recommended

#       restorbeam|['']     use a specified restor beam for imaging
#                           default values are calculated from invert results
#       minpb|0.1           cutoff for pb correction
#       gridemode|'aprojection'
#
#       cleancont|False     MFS Imaging for the continuum data
#       cleanspec|True      channel by channel imaging for the spectral line data
#
#       mweight|False       mosweight=True to better deal with few fields+ different
#                           nosie level case in the archival data#
#
#   HISTORY
#
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
xu.news("------------- Begin Task: xclean "+xp['prefix']+" -------------")
xu.news("++")
xu.news("")
casa_log = open(casalog.logfile(),'r')
startlog = casa_log.readlines()
casa_log.close()

#----------------------------------------------------------------------------------------
#   Default Values for Optional Inputs
#----------------------------------------------------------------------------------------
if  type(xp['imsize'])==type(0):
    imsize=[xp['imsize'],xp['imsize']]
if  type(xp['imsize'])==type([]):
    imsize=xp['imsize']


innerquarter=str(int(imsize[0]/4))+','+str(int(imsize[1]/4))+','\
            +str(int(imsize[0]*3/4))+','+str(int(imsize[1]*3/4))
outerquarter=str(0)+','+str(0)+','\
            +str(int(imsize[0]*1/4))+','+str(int(imsize[1]*1/4))+','\
            +str(0)+','+str(int(imsize[1]*3/4))+','\
            +str(int(imsize[0]*1/4))+','+str(int(imsize[1]-1))+','\
            +str(int(imsize[0]*3/4))+','+str(0)+','\
            +str(int(imsize[0]-1))+','+str(int(imsize[1]*1/4))+','\
            +str(int(imsize[0]*3/4))+','+str(int(imsize[1]*3/4))+','\
            +str(int(imsize[0]-1))+','+str(int(imsize[1]-1))    
if  xp['imstat_box_spec']=='':
    xp['imstat_box_spec']=innerquarter    
    if  xp['imcs']==True:
        xp['imstat_box_spec']=outerquarter
if  xp['imstat_box_cont']=='':
    xp['imstat_box_cont']=outerquarter


xp['srcfile']=xp['prefix']+'.src.ms'
if  xp['imagermode']==None:
    xp['imagermode']='csclean'
    
    prepvis=xp['srcfile']
    if  xp['uvcs']==True:
        prepvis=xp['srcfile']+'.contsub'
    
    tb.open(prepvis+'/FIELD')
    nfield=len(tb.getcol('NAME'))
    tb.close()
    if  nfield>1:
        imagermode = 'mosaic'    
    hetero=False
    xu.news("")
    xu.news("nfield: "+str(nfield))
    
    tb.open(prepvis+"/OBSERVATION")
    obsnamelist=tb.getcol("TELESCOPE_NAME")
    xu.news("obsname_list:"+str(obsnamelist))
    xu.news("")
    for obsname in obsnamelist:
        if  obsname=='ALMA' or obsname=='CARMA':
            xp['imagermode']='mosaic'
            xp['ftmachine']='mosaic'
    tb.close()
    xu.news("imagermode -> "+xp['imagermode'])
    xu.news("ftmachine  -> "+xp['ftmachine'])
    xu.news("")

if  xp['uvcs']==True:
    xp['cleancont']=True

#----------------------------------------------------------------------------------------
#   Make a dirty spectral cube, and determine the cube sigma level
#----------------------------------------------------------------------------------------

vis_loop=[]
outname_loop=[]
niter_loop=[]
threshold_loop=[]
cleanmode_loop=[]
cleanspw_loop=[]
restorbeam_loop=[]
resmooth_loop=[]
multiscale_loop=[]

if  xp['cleanspec']==True:
    
    if  xp['uvcs']==True:
        vis=xp['srcfile']+'.contsub'
    else:
        vis=xp['srcfile']
    if  xp['imcs']==True:
        outname=xp['prefix']+'.coli'
    else:
        outname=xp['prefix']+'.line'
    
    if  xp['threshold_spec']=='0.0mJy' and xp['niter']!=0:
        vis_loop+=[vis]
        outname_loop+=[outname+'_d']
        niter_loop+=[0]
        threshold_loop+=['0.0mJy']
        cleanmode_loop+=[xp['cleanmode']]
        cleanspw_loop+=[xp['cleanspw']]
        restorbeam_loop+=[xp['restorbeam']]
        resmooth_loop+=['']
        multiscale_loop+=[[]]

    vis_loop+=[vis]
    outname_loop+=[outname]
    niter_loop+=[xp['niter']]
    threshold_loop+=[xp['threshold_spec']]
    cleanmode_loop+=[xp['cleanmode']]
    cleanspw_loop+=[xp['cleanspw']]
    restorbeam_loop+=[xp['restorbeam']]
    resmooth_loop+=[xp['resmooth']]
    multiscale_loop+=[xp['multiscale']]

if  xp['cleancont']==True:
    
    vis=xp['srcfile']
    outname=xp['prefix']+'.cont'
    if  xp['uvcs']==True:
        spw=xp['fitspw']
    else:
        spw=''
    if  xp['threshold_cont']=='0.0mJy' and xp['niter']!=0:
        vis_loop+=[vis]
        outname_loop+=[outname+'_d']
        niter_loop+=[0]
        threshold_loop+=['0.0mJy']
        cleanmode_loop+=['mfs']
        cleanspw_loop+=[spw]
        restorbeam_loop+=[xp['restorbeam']]
        resmooth_loop+=['']
        multiscale_loop+=[[]]

    vis_loop+=[vis]
    outname_loop+=[outname]
    niter_loop+=[xp['niter']]
    threshold_loop+=[xp['threshold_cont']]
    cleanmode_loop+=['mfs']
    cleanspw_loop+=[spw]
    restorbeam_loop+=[xp['restorbeam']]
    resmooth_loop+=['']
    multiscale_loop+=[xp['multiscale']]

for i in range(0,len(vis_loop)):
    
    xu.news("")
    xu.news("--clean--")
    xu.news("")
    xu.news("Make a line cube (pb uncorreted)")
    xu.news("")
    
    xu.cleanup(outname_loop[i])        

    start=xp['clean_start']
    width=xp['clean_width']
    if  cleanmode_loop[i]=='mfs':
        start=0
        width=1
    clean(vis=vis_loop[i],
          imagename=outname_loop[i],
          field=xp['clean_field'],
          spw=cleanspw_loop[i],
          mode=cleanmode_loop[i],
          nchan=xp['clean_nchan'],
          start=start,
          width=width,
          niter=niter_loop[i],
          intent="",
          resmooth=resmooth_loop[i],
          multiscale=multiscale_loop[i],
          negcomponent=xp['negcomponent'],
          interpolation=xp['spinterpmode'],
          threshold=threshold_loop[i],
          psfmode=xp['psfmode'],
          mask=xp['clean_mask'],
          imsize=xp['imsize'],
          cell=xp['cell'],
          weighting=xp['cleanweight'],
          robust =xp['wrobust'],
          imagermode=xp['imagermode'],
          phasecenter=xp['phasecenter'],
          ftmachine=xp['ftmachine'],
          outframe=xp['outframe'],
          restfreq=xp['restfreq'],
          scaletype='SAULT',
          mosweight=xp['mweight'],
          minpb=xp['minpb'],
          pbcor=False,
          uvtaper=True,
          outertaper=xp['outertaper'],
          cyclefactor=xp['cyclefactor'],
          restoringbeam=restorbeam_loop[i],
          gain=xp['clean_gain'],
          stokes='I',
          chaniter=xp['iterchan'],
          allowchunk=xp['allowchunk'],
          usescratch=xp['usescratch'],
          selectdata=True)
    xu.modelconv(outname_loop[i])

    xu.news("")
    xu.news("")   
    xu.news("--imstat--")
    xu.news("")
    xu.news(" Determine the line cube sigma level (pb uncorreted)")
    xu.news("")
    
    if  cleanmode_loop[i]!='mfs':
        ds_stat=imstat(imagename=outname_loop[i]+'.image',
                       box=xp['imstat_box_spec'],
                       chans=xp['imstat_chan'],
                       axes=[0,1],
                       region=xp['imstat_rg_spec'])
        sigmjy=np.median(ds_stat['sigma'])*1000.
        if  outname_loop[i][-2:]=='_d':
            if  threshold_loop[i+1]=='0.0mJy':
                threshold_loop[i+1]=str(sigmjy*xp['sigcutoff_spec'])+'mJy'
            #    resmooth='common' might be better than hacking <restorbeam> on 
            #    maching flux scales in model & residual
            #
            #if  restorbeam_loop[i+1]==['']:
            #    restorbeam_loop[i+1]=\
            #        xu.checkbeam(outname_loop[i],method=xp['restorbeam_method'])
    else:
        dc_stat=imstat(imagename=outname_loop[i]+'.image',
                       box=xp['imstat_box_cont'],
                       region=xp['imstat_rg_cont'])
        sigmjy=dc_stat['sigma'][0]*1000.
        if  outname_loop[i][-2:]=='_d':
            if  threshold_loop[i+1]=='0.0mJy':
                threshold_loop[i+1]=str(sigmjy*xp['sigcutoff_cont'])+'mJy'
            #    resmooth='common' might be better than hacking <restorbeam> on 
            #    maching flux scales in model & residual
            #
            #if  restorbeam_loop[i+1]==['']:
            #    restorbeam_loop[i+1]=\
            #        xu.checkbeam(outname_loop[i],method=xp['restorbeam_method'])
    
    xu.news("")
    xu.news("-------------------------------------------------------------------------")
    xu.news(" Found the normalized sigma = "+str(sigmjy)+"mJy/beam")
    xu.news("-------------------------------------------------------------------------")
    xu.news("")
    
    imhead(imagename=outname_loop[i]+'.image')
    immath(imagename=[outname_loop[i]+'.image',outname_loop[i]+'.flux'],
           expr='IM0/IM1',
           outfile=outname_loop[i]+'.cm')
    
    xu.exporttasklog('imhead',outname_loop[i]+'.image.imhead.log')
    xu.exporttasklog('imstat',outname_loop[i]+'.image.imstat.log')
    xu.exporttasklog('clean',outname_loop[i]+'.image.iteration.log')
    os.system("cp -rf clean.last "+outname_loop[i]+'.image.clean.log')

#----------------------------------------------------------------------------------------
#   image-domain continuum substraction
#----------------------------------------------------------------------------------------
if  xp['imcs']==True:   

    xu.news("")
    xu.news("--imcontsub--")
    xu.news("")
    xu.news("Continumm substraction in the cube")
    xu.news("")

    outname = xp['prefix']
    os.system('rm -rf '+outname+'.cont.* ')
    os.system('rm -rf '+outname+'.line.* ')
 
    mask0=outname+'.coli.flux'
    xu.genmask0(mask0)
    xu.mask0clean(outname+'.coli',mask0+'.mask0')
    
    imcontsub(imagename=outname+'.coli.cm',
              linefile=outname+'.line.cm',
              contfile=outname+'.cont.cm.cube',
              fitorder=xp['fitorder'],
              chans=xp['fitchans'])
    xu.news("")
    
    immoments(imagename=outname+'.coli.cm',
              outfile=outname+'.cont.cm',
              chans=xp['fitchans'],
              moments=-1)
    
    os.system('rm -rf '+outname+'.line.flux ')
    os.system('cp -rf '+outname+'.coli.flux '+outname+'.line.flux')
    immath(imagename=[outname+'.line.cm',outname+'.line.flux'],
           expr='IM0*IM1',
           outfile=outname+'.line.image')
    
    os.system('rm -rf '+outname+'.cont.flux ')        
    immath(imagename=[outname+'.cont.cm.cube',outname+'.coli.flux'],
           expr='IM0*IM1',
           outfile=outname+'.cont.image.cube')
    
    os.system('rm -rf flux.tmp?')
    immath(imagename=[outname+'.line.flux'],
           expr='1/(IM0^2)',
           outfile='flux.tmp0')
    immoments(imagename='flux.tmp0',
              outfile='flux.tmp1',
              chans=xp['fitchans'],
              moments=-1)
    immath(imagename=['flux.tmp1'],
           outfile='flux.tmp2',
           expr='1/(IM0^0.5)')
    pbstat=imstat('flux.tmp2')
    pbmax=pbstat['max'][0]
    immath(imagename=['flux.tmp2'],
           outfile=outname+'.cont.flux',
           expr='IM0/'+str(pbmax))
    os.system('rm -rf flux.tmp?')   
    
    immath(imagename=[outname+'.cont.cm',outname+'.cont.flux'],expr='IM0*IM1',\
           outfile=outname+'.cont.image')


    xu.news("")
    xu.news("")   
    xu.news("--imstat--")
    xu.news("")
    xu.news(" Determine the line cube sigma level (pb uncorreted)")
    xu.news("")
    

    ds_stat=imstat(imagename=outname+'.line.image',
                   box=xp['imstat_box_spec'],
                   chans=xp['imstat_chan'],
                   axes=[0,1],
                   region=xp['imstat_rg_spec'])
    sigmjy=np.median(ds_stat['sigma'])*1000.
    xu.news("")
    xu.news("-------------------------------------------------------------------------")
    xu.news(" Found the normalized sigma = "+str(sigmjy)+"mJy/beam")
    xu.news("-------------------------------------------------------------------------")
    xu.news("")

    imhead(imagename=outname+'.line.image')
    xu.exporttasklog('imhead',outname+'.line.image.imhead.log')
    xu.exporttasklog('imstat',outname+'.line.image.imstat.log')
 

    
    dc_stat=imstat(imagename=outname+'.cont.image',
                   box=xp['imstat_box_cont'],
                   region=xp['imstat_rg_cont'])
    sigmjy=dc_stat['sigma'][0]*1000.
    xu.news("")
    xu.news("-------------------------------------------------------------------------")
    xu.news(" Found the normalized sigma = "+str(sigmjy)+"mJy/beam")
    xu.news("-------------------------------------------------------------------------")
    xu.news("")
    
    imhead(imagename=outname+'.cont.image')
    xu.exporttasklog('imhead',outname+'.cont.image.imhead.log')
    xu.exporttasklog('imstat',outname+'.cont.image.imstat.log')


xu.news("")
xu.news("--exportfits--")
xu.news("")
xu.news("Export all images to FITS format")
xu.news("")
xu.exportclean(xp['prefix']+'.line_d',keepcasaimage=xp['keepcasaimage'])
xu.exportclean(xp['prefix']+'.line',keepcasaimage=xp['keepcasaimage'])
xu.exportclean(xp['prefix']+'.cont_d',keepcasaimage=xp['keepcasaimage'])
xu.exportclean(xp['prefix']+'.cont',keepcasaimage=xp['keepcasaimage'])
xu.exportclean(xp['prefix']+'.coli_d',keepcasaimage=xp['keepcasaimage'])
xu.exportclean(xp['prefix']+'.coli',keepcasaimage=xp['keepcasaimage'])
xu.news("")

#----------------------------------------------------------------------------------------
#   End Statement
#----------------------------------------------------------------------------------------
subima2time=time.time()
xu.news("")
xu.news("Total Imaging Time: %10.1f" %(subima2time-startTime))
xu.news("")
xu.news("++")
xu.news("------------- End Task: xclean "+xp['prefix']+" -------------")
xu.news("++")
xu.news("")
casa_log=open(casalog.logfile(),'r')
stoplog=casa_log.readlines()
casa_log.close()
xu.exportcasalog(startlog,stoplog,xp['prefix']+'.xclean.reduc.log')

if  xp['email']!='':
    emailsender(xp['email'],\
                "RUN xclean End: "+xp['prefix'],\
                "This email was generated automatically \
                by your successful reduction run.\nThe log files are attached",\
                [xp['prefix']+'.xclean.reduc.log'])
